# 🎮 StreamDeck Setup Guide for ReadAloud

## 🚀 **Quick Setup (Recommended)**

### **Step 1: Create StreamDeck Buttons**

In your StreamDeck software, create new buttons and set them to **"Open"** or **"System"** actions:

#### **Button 1: Read Clipboard**
- **Action Type**: System → Open
- **File Path**: `C:\Project\ki-fu\readaloud\streamdeck\actions\read_clipboard.bat`
- **Icon**: 📋 (or any clipboard icon)
- **Title**: "Read Clipboard"

#### **Button 2: Read Selection**
- **Action Type**: System → Open
- **File Path**: `C:\Project\ki-fu\readaloud\streamdeck\actions\read_selection.bat`
- **Icon**: 📝 (or any text selection icon)
- **Title**: "Read Selection"

#### **Button 3: Stop Audio**
- **Action Type**: System → Open
- **File Path**: `C:\Project\ki-fu\readaloud\streamdeck\actions\stop_audio.bat`
- **Icon**: ⏹️ (or any stop icon)
- **Title**: "Stop Audio"

#### **Button 4: Read File**
- **Action Type**: System → Open
- **File Path**: `C:\Project\ki-fu\readaloud\streamdeck\actions\read_file.bat`
- **Icon**: 📄 (or any file icon)
- **Title**: "Read File"

### **Step 2: Test Your Buttons**

1. **Copy some text** to your clipboard
2. **Press the "Read Clipboard" button** on your StreamDeck
3. **Select some text** in any application
4. **Press the "Read Selection" button** on your StreamDeck

## 🔧 **Advanced Setup Options**

### **Option A: Custom File Paths**

To read specific files, edit `read_file.bat` and change the `FILE_PATH` variable:

```batch
set FILE_PATH="C:\Users\YourName\Documents\important.txt"
```

### **Option B: Multiple File Buttons**

Create multiple buttons for different files:

- `read_file_notes.bat` → `set FILE_PATH="C:\Notes\daily.txt"`
- `read_file_emails.bat` → `set FILE_PATH="C:\Emails\inbox.txt"`

### **Option C: Custom Actions**

You can create custom actions by editing `simple_integration.py` and adding new functions.

## 🎯 **How It Works**

1. **StreamDeck button press** → Executes the `.bat` file
2. **Batch file** → Changes to ReadAloud directory and runs Python script
3. **Python script** → Calls ReadAloud with specific action
4. **ReadAloud** → Uses Higgs Audio to generate and play speech

## 🚨 **Troubleshooting**

### **Button Not Working?**
- Check that the file paths in StreamDeck are correct
- Make sure Python is in your system PATH
- Verify that `readaloud_config.json` exists

### **No Audio Output?**
- Run `python main.py --info` to check Higgs Audio setup
- Check that your audio device is working
- Verify the configuration in `readaloud_config.json`

### **Permission Errors?**
- Run StreamDeck as Administrator
- Check that the batch files have execute permissions

## 🎨 **Button Layout Suggestions**

### **Minimal Setup (4 buttons)**
```
[📋] [📝] [⏹️] [📄]
```

### **Extended Setup (6 buttons)**
```
[📋] [📝] [⏹️] [📄] [👁️] [⚡]
```

## 🔄 **Next Steps**

1. **Test basic functionality** with the 4 main buttons
2. **Customize file paths** for your specific needs
3. **Create additional buttons** for frequently used files
4. **Set up profiles** for different use cases

## 📞 **Need Help?**

If you encounter issues:
1. Check the console output when pressing buttons
2. Verify all file paths are correct
3. Test ReadAloud manually first: `python main.py --interactive`
4. Check that Higgs Audio is working: `python main.py --info`
