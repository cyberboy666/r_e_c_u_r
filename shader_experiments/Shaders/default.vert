// this is the default.vert shader used by conjur , it ensures that the frag shaders run by glslViewer will also run in openframeworks
attribute vec4 position;
attribute vec4  color;
attribute vec3  normal;
attribute vec2 texcoord;

uniform mat4 modelViewProjectionMatrix;

varying vec4 v_position;
varying vec4    v_color;
varying vec3    v_normal;
varying vec2 v_texcoord;

uniform mat4 u_modelViewProjectionMatrix;

void main() {
    v_position = position;
    v_color = color;
    v_normal = normal;
    v_texcoord = texcoord;

    gl_Position = modelViewProjectionMatrix * position;

}
