attribute vec4 position;
attribute vec2 texcoord;
uniform mat4 modelViewProjectionMatrix;

varying vec2 texcoord0;

void main() {
    gl_Position = modelViewProjectionMatrix * position;
    texcoord0 = texcoord;
}
