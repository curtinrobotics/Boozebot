#include <Arduino.h>
#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <NfcAdapter.h>

/* Constants */
#define TIMEOUT_LIMIT 3 // How many read attempts to try before timing out
#define MIFARE_BlOCK 56 // The MIFARE block containing the student ID

/* Function Prototypes */
boolean readBlock(uint8_t block, char *data, uint8_t *uid, uint8_t uidLength, uint8_t *key);

/* NFC Objects */
PN532_I2C pn532i2c(Wire);
PN532 nfc(pn532i2c);

// Keep record of the last scanned ID, so a card won't be scanned multiple times in a row
// Assumed that all IDs are at most 8 characters long (+ a null terminator)
char lastId[9];

void setup() {
  Serial.begin(115200);

  nfc.begin();

  // Try retrieve data from the attached PN532 board
  uint32_t versiondata = nfc.getFirmwareVersion();

  if (!versiondata) {
    Serial.println("No PN532 board found. Halting.");
    while (1); // Halt
  }

  // Set the max number of retry attempts to read from a card
  // This prevents us from waiting forever for a card, which is
  // the default behaviour of the PN532.
  nfc.setPassiveActivationRetries(0xFF);

  // Configure board to read RFID tags
  nfc.SAMConfig();
}

void loop() {
  static int timeoutCounter = 0;

  uint8_t success;                          // Flag to check if there was an error with the PN532
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  char data[16];                            // Array to store block data during reads

  // Keyb on NDEF and MIFARE Classic should be the same
  uint8_t blockKey[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };
  uint8_t block = MIFARE_BlOCK;

  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);

  if (success) {
    // Attempt to read from the ID block
    success = readBlock(block, data, uid, uidLength, blockKey);

    if (success) {
      char* userId = (data);

      // Reset the timeout counter
      timeoutCounter = 0;

      // Make sure this ID hasn't just been scanned
      if(strncmp(lastId, userId, 9) != 0) {
        Serial.println(userId);
        strncpy(lastId, userId, 9);
      }
    }
  } else {
    // If no card is being read, clear the last read ID
    strcpy(lastId, "");

    timeoutCounter++;

    if(timeoutCounter >= TIMEOUT_LIMIT) {
      Serial.println("timeout");
      timeoutCounter = 0;
    }
  }
}

boolean readBlock(uint8_t block, char *data, uint8_t *uid, uint8_t uidLength, uint8_t *key) {
  boolean authed = nfc.mifareclassic_AuthenticateBlock(uid, uidLength, block, 0, key);
  if (authed) {
    boolean readSuccess = nfc.mifareclassic_ReadDataBlock(block, data);
    if (readSuccess) {
      return true;
    }
  }
  return false;
}
