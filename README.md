# eTFT GIF Converter

GIF to header (.h) generator for the ESP32 eTFT screens.


## Changelog
	v0.2 (12/24/2021)
		Added Windows/Linux Interoperability
		Added built-in resizing using arguments (-width / -height)
		Added additional argument to specify ImageMagick directory	(-imdir)

    
## Pre-requisites

Install [ImageMagick](https://imagemagick.org/), making sure you check the "Install legacy utilities (e.g. convert)" option in the installer.
<img src="https://github.com/EdwardKrayer/esp32-etft-gif-converter/raw/main/img/imagemagick-installer.png">


## Command Line Usage

```
eTFT-gif-converter.py
				-i <GIF>                                                  Required
				-o <OUTPUT_HEADER_FILE.H>									                Required
				[-width <MAX PIXEL WIDTH OF TFT>]							            Optional, defaults to 320
				[-height <MAX PIXEL HEIGHT OF TFT>]							          Optional, defaults to 240
				[-imdir <LOCATION OF IMAGE MAGICK CONVERT EXECUTABLE>]		Optional, defaults to "C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/" or "/usr/bin/"
```


## Example (Windows)

```python
./eTFT-gif-converter.py -i example/starcraft.gif -o starcraft.h -width 320 -height 240 -imdir "C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/"
```


## Example (Linux)

```python
./eTFT-gif-converter.py -i example/starcraft.gif -o starcraft.h -width 320 -height 240 -imdir "/usr/bin/"
```


### Complete Example

```bash
git clone https://github.com/EdwardKrayer/esp32-etft-gif-converter.git
cd esp32-etft-gif-converter.git
pip3 install -r requirements.txt
python3 ./eTFT-gif-converter.py -i example/starcraft.gif -o starcraft.h -width 320 -height 240 -imdir "C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/"
```


### Adding it to Arduino / PlatformIO / C++ 

You could be use the **animation.h** header generated like this:

```C++

#include "animation.h"

void loop() {
    if(shutdown++ > 5) espDeepSleep();
    for (int i = 0; i < frames; i++) {
        tft.pushImage(
          2,                   // x position
          0,                   // y position
          animation_width, 
          animation_height, 
          animation[i]
        );
        delay(120);
    }
}
```


## Thanks to Original Author / Project
Alex Arce @ [https://github.com/alex-arce/esp32-etft-gif-converter/](https://github.com/alex-arce/esp32-etft-gif-converter/)