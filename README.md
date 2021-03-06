# Tangent
A simple tool to insert images into a text box on any chat application. Made with Python and PyQt5 and is still a work in progress.

**Why I made this tool:**

-This tool was made as I had a dedicated reaction folder on my local storage. I would use it constantly when chatting with friends. While I could add the images as custom stickers in specific chat applications, it would only be usable on that specific platform.

**How does it work:**

-Tangent reads a single folder and displays all valid file formats as images into the application and is applicable for any text window that accepts images as an input. This tool can be used on Facebook Messanger, Whatsapp and Discord

-Once Tangent has started, it will disappear from the taskbar when not in focus. To activate it, the current bound hotkey is "alt + q".

-Tangent will remain in the background and can be closed via the tray icon options

**Steps to use**
1) Start up the application
2) Press alt + q while the mouse cursor is hovering over the respective text box
3) Double click on the selected image


![image](https://user-images.githubusercontent.com/54271305/175807110-835e29eb-4ee5-4ae7-b471-90f6c3df330a.png)

3) The selected image will be pasted and sent as an image message. (Short Demo in Whatsapp)

https://user-images.githubusercontent.com/54271305/175817353-1af32ca3-dbaa-4690-b866-c62b0eaa8729.mov


4) When not in focus, Tangent will be hidden away from the taskbar and remain active in the tray icons menu using PyQt's icon

![image](https://user-images.githubusercontent.com/54271305/175807148-7099716d-159b-4cbd-ae05-2b6293d4e8fa.png)


Current Limitations:
1) Users have to ensure that the mouse cursor is hovering over the text box when pressing the hotkey "alt+q"
2) Only image files like jpg and pngs are usable in the tool. Gifs and videos are not supported yet

More features to come soon!




