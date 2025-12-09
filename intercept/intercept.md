## 🛡️ BurpSuite Interception Guide for SecureChat APK

This guide outlines the steps to configure an Android 14 (API 34) emulator, install the Burp Suite CA certificate as a system trusted credential, and use Frida to bypass potential security controls, enabling Burp Suite to intercept traffic from the `SecureChat` APK.

-----

### 📋 Requirements

  * **Android Studio** with **SDK Android (API 34)** and necessary tools (**SDK Build tools, SDK platform tools**).
  * **Burp Suite Community Edition** (or Professional).
  * **Frida** and **frida-tools** installed on your host machine.

-----

### 📱 Creating and Launching Your Phone (Emulator)

1.  **Install Dependencies:** Ensure **SDK android (API 34)** and required tools (**SDK Build tools, SDK platform tools**) are installed via the SDK Manager in Android Studio.
2.  **Add New Device:** Create a new Virtual Device (AVD).
      * **API:** Choose **API 34**.
      * **Services:** Select **Google API**.
      * **System Image:** Choose a system image like **Google APIs...** (e.g., `x86_64` or `arm64-v8a`).
3.  **Finish** the configuration and **Launch** the emulator.
4.  **Install APK:** Install the `SecureChat` APK onto the running emulator using `adb install SecureChat.apk`.

-----

### 🔒 Creating Certificates and Installing as Trusted

1.  **Launch Burp Suite:** Start Burp Suite and configure the **Proxy** listener.
2.  **Configure Proxy:**
      * Choose your interfaces (e.g., **All interfaces** or the **IPv4** address of your PC).
      * Select an **unused port** (e.g., `8080`).
    -----
3.  **Export Certificate:**
      * Navigate to **Proxy -\> Options -\> Import/Export CA Certificate**.
      * Click **"Export Certificate in DER format"**.
      * Save the certificate to a known location on your host PC (e.g., `cacert.der`).
4.  **Install Certificate:** Android 14 (API 34) requires specific steps to install a CA as a **system-trusted credential**. Follow a guide like the one referenced:
      * `https://httptoolkit.com/blog/android-14-install-system-ca-certificate/#how-to-install-system-ca-certificates-in-android-14`
      * **Push the Certificate:** Use **ADB** to push the exported certificate to the device. Remember its location and name.
      * **Run Commands:** Use the ADB shell to copy the cert into the system's trusted store and adjust permissions.
5.  **Confirmation:** On the emulator, navigate to **Settings** and confirm that the "PortSwigger" CA is listed inside **"Trusted Credentials"** (under the "System" tab).

-----

### ⚙️ Installing Frida Server

1.  **Launch Phone:** Ensure the emulator is running.
2.  **Download Server:** Download the correct Frida Server binary for your emulator's architecture (e.g., `frida-server-17.5.1-android-x86_64.xz`). Extract it.
3.  **Push Server:** Use ADB to push the extracted server binary to the emulator's temporary directory:
    ```bash
    adb push "/path/to/frida-server-17.5.1-android-x86_64" /data/local/tmp/
    ```
4.  **Run Server:** Access the shell and execute the server:
    ```bash
    adb shell
    su
    chmod 755 /data/local/tmp/frida-server-17.5.1-android-x86_64
    /data/local/tmp/frida-server-17.5.1-android-x86_64
    ```
    > **⚠️ IMPORTANT:** **KEEP THIS TERMINAL ALIVE** while you are running the app and performing interception.

-----

### 💻 Running Frida for Interception

1.  **Verify Frida:** On your host machine, confirm Frida is installed:
    ```bash
    frida --version
    ```
2.  **Prepare Script:** Download the necessary "fridascript.js" (likely a script to bypass certificate pinning) and **edit the following line** to correctly point to the path and name of the certificate you pushed to the device:
    ```javascript
    var fileInputStream = FileInputStream.$new("/data/local/tmp/<your-cert-name>");
    ```
3.  **Execute Frida:** Run the app with the Frida script attached:
    ```bash
    frida -U -f com.example.securechat -l "path/to/fridascript.js"
    ```
      * `-U`: Connects to a USB device (works for an emulator when only one is running).
      * `-f`: Spawns the application and injects the script.
      * `-l`: Loads the script.
4.  **Complete Launch:** Once the app is spawned, you may need to enter specific prompts, such as:
    ```
    Enter group-id: group-2
    ```

-----