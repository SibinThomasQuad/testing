from selenium import webdriver
from PIL import Image
import time

# Define the website URL
url = "https://example.com"  # Replace with the URL you want to test

# Define device dimensions for different devices
devices = {
    "Mobile": (360, 640),
    "Tablet": (768, 1024),
    "Laptop": (1366, 768),
    "iPad": (768, 1024),
}

# Create a web driver (change to Chrome or other supported browsers as needed)
driver = webdriver.Firefox()

# Loop through devices and capture screenshots
for device, (width, height) in devices.items():
    driver.set_window_size(width, height)
    driver.get(url)
    time.sleep(2)  # Give the page time to adjust

    # Capture a screenshot and save it
    screenshot_filename = f"screenshot_{device}.png"
    driver.save_screenshot(screenshot_filename)

# Close the web driver
driver.quit()

# Merge screenshots into a single image
images = [Image.open(f"screenshot_{device}.png") for device in devices]
combined_image = Image.new("RGB", (max(image.width for image in images), sum(image.height for image in images)))
y_offset = 0
for image in images:
    combined_image.paste(image, (0, y_offset))
    y_offset += image.height

combined_image.save("combined_screenshot.png")

print("Screenshots captured and combined.")
