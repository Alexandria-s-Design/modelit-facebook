/**
 * Google Apps Script to Update Sheet with Image URLs from Drive Folder
 *
 * Installation:
 * 1. Open Google Sheet: https://docs.google.com/spreadsheets/d/1pjJl8yxdVi-HwdkFxuu5Uq2qPklYAicX67sLz8qHCV0
 * 2. Extensions → Apps Script
 * 3. Paste this code and save
 * 4. Run updateImageURLs function
 * 5. Authorize when prompted
 */

function updateImageURLs() {
  const SHEET_ID = '1pjJl8yxdVi-HwdkFxuu5Uq2qPklYAicX67sLz8qHCV0';
  const FOLDER_ID = '1JAEQPbWPEQKb3oU3BvN7bRGwT0ZrgW5I';

  try {
    Logger.log('Starting image URL update...');

    // Get the sheet
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const sheet = ss.getSheetByName('Sheet1') || ss.getSheets()[0];

    // Get the Drive folder
    const folder = DriveApp.getFolderById(FOLDER_ID);
    const files = folder.getFiles();

    // Build a map of filename → URL
    const urlMap = {};
    let fileCount = 0;

    while (files.hasNext()) {
      const file = files.next();
      const filename = file.getName();

      // Get shareable link
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
      const url = file.getUrl();

      // Convert to direct image URL for embedding
      const fileId = file.getId();
      const directUrl = `https://drive.google.com/uc?export=view&id=${fileId}`;

      urlMap[filename] = directUrl;
      fileCount++;
    }

    Logger.log(`Found ${fileCount} files in Drive folder`);

    // Read existing sheet data
    const dataRange = sheet.getRange('A2:I105'); // Rows 2-105 (104 posts)
    const data = dataRange.getValues();

    let updated = 0;
    let missing = 0;

    // Update each row
    for (let i = 0; i < data.length; i++) {
      const row = data[i];
      const postNumber = row[0]; // Column A
      const imageFilename = row[8]; // Column I (image_filename)

      if (imageFilename && urlMap[imageFilename]) {
        // Update column H (image_url)
        row[7] = urlMap[imageFilename];
        updated++;
      } else if (imageFilename) {
        Logger.log(`Missing file: ${imageFilename}`);
        missing++;
      }
    }

    // Write back to sheet
    dataRange.setValues(data);

    // Log results
    Logger.log('='.repeat(50));
    Logger.log('UPDATE COMPLETE');
    Logger.log('='.repeat(50));
    Logger.log(`Files in Drive: ${fileCount}`);
    Logger.log(`URLs updated: ${updated}`);
    Logger.log(`Missing files: ${missing}`);

    // Show user message
    SpreadsheetApp.getActiveSpreadsheet().toast(
      `Updated ${updated} image URLs successfully! ${missing} files missing.`,
      'Image URL Update Complete',
      10
    );

  } catch (error) {
    Logger.log(`ERROR: ${error.toString()}`);
    SpreadsheetApp.getActiveSpreadsheet().toast(
      `Error: ${error.toString()}`,
      'Update Failed',
      10
    );
  }
}

/**
 * Create a menu when the spreadsheet opens
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Image Tools')
    .addItem('Update Image URLs from Drive', 'updateImageURLs')
    .addToUi();
}

/**
 * Manual function to list all files in the Drive folder
 * Useful for debugging
 */
function listDriveFiles() {
  const FOLDER_ID = '1JAEQPbWPEQKb3oU3BvN7bRGwT0ZrgW5I';
  const folder = DriveApp.getFolderById(FOLDER_ID);
  const files = folder.getFiles();

  Logger.log('Files in Drive folder:');
  Logger.log('='.repeat(50));

  let count = 0;
  while (files.hasNext()) {
    const file = files.next();
    Logger.log(`${++count}. ${file.getName()}`);
    Logger.log(`   URL: ${file.getUrl()}`);
    Logger.log(`   ID: ${file.getId()}`);
  }

  Logger.log('='.repeat(50));
  Logger.log(`Total files: ${count}`);
}
