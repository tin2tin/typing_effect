bl_info = {
    "name": "Typing Effect for VSE Text Strips",
    "description": "Adds a typing animation effect to VSE text strips based on strip timings.",
    "author": "tintwotin",
    "version": (1, 0, 4),
    "blender": (3, 0, 0),
    "location": "Video Sequence Editor > Sidebar > Effect Strip",
    "category": "Sequencer",
}

import bpy

# Typing animation handler
def typing_animation_handler(scene):
    vse = scene.sequence_editor
    if not vse:
        return

    for strip in vse.sequences_all:
        if strip.type == 'TEXT' and strip.get('typing_effect_enabled'):
            # Calculate progress based on strip timing
            progress = (scene.frame_current - strip.frame_start) / (strip.frame_final_end - strip.frame_start)
            
            # Ensure progress is within bounds
            if progress < 0:
                continue
            elif progress > 1:
                progress = 1.1  # Cap progress to 100%

            # Update the text to display based on progress
            full_text = strip.typing_effect_text
            visible_length = int(len(full_text) * progress)+1
            strip.text = full_text[:visible_length]

# Sync typing_effect_text with text when enabling/disabling the effect
def toggle_typing_effect(self, context):
    strip = context.scene.sequence_editor.active_strip
    if strip and strip.type == 'TEXT':
        if strip.typing_effect_enabled:
            # Copy current text to typing_effect_text when enabling
            strip.typing_effect_text = strip.text
            register_handlers()
        else:
            # Copy typing_effect_text back to text when disabling
            strip.text = strip.typing_effect_text
            unregister_handlers()

# Draw function to prepend UI elements
def draw_typing_effect_ui(self, context):
    layout = self.layout
    strip = context.scene.sequence_editor.active_strip

    if strip and strip.type == 'TEXT':
        layout.separator()
        row = layout.row()
        row.prop(strip, "typing_effect_enabled")

# Register the handler for frame changes
def register_handlers():
    if typing_animation_handler not in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.append(typing_animation_handler)
    if typing_animation_handler not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(typing_animation_handler)

# Unregister the handler for frame changes
def unregister_handlers():
    if typing_animation_handler in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.remove(typing_animation_handler)
    if typing_animation_handler in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(typing_animation_handler)

# Append properties to text strips
def append_properties():
    bpy.types.Sequence.typing_effect_enabled = bpy.props.BoolProperty(
        name="Typing Effect",
        description="Enable typing animation for this text strip based on strip timings",
        default=False,
        update=toggle_typing_effect,  # Trigger sync logic
    )
    bpy.types.Sequence.typing_effect_text = bpy.props.StringProperty(
        name="Typing Effect Text",
        description="The text used for the typing effect",
        default="",
    )

# Remove properties
def remove_properties():
    del bpy.types.Sequence.typing_effect_enabled
    del bpy.types.Sequence.typing_effect_text

# Register add-on classes and handlers
def register():
    append_properties()
    bpy.types.SEQUENCER_PT_effect.append(draw_typing_effect_ui)  # Prepend the custom UI
    register_handlers()

# Unregister add-on classes and handlers
def unregister():
    unregister_handlers()
    remove_properties()
    bpy.types.SEQUENCER_PT_effect.remove(draw_typing_effect_ui)  # Remove the custom UI

if __name__ == "__main__":
    register()
