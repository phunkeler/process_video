from moviepy.editor import ImageClip

input_file = "original.png"
output_file = "output.mp4"
width = 200  # Desired width
height = 200  # Desired height

# Load the image clip
image_clip = ImageClip(input_file)

# Resize the image clip
resized_clip = image_clip.resize(width=width, height=height)

# Set the duration of the resized clip to match the original duration
resized_clip = resized_clip.set_duration(image_clip.duration)

# Write the resized clip to the output file
resized_clip.write_videofile(output_file)
