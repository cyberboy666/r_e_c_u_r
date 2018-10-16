//pro-shader
//written by Tim Caldwell
// this is a simple example of how to change incoming textures colour
varying vec2 v_texcoord;
uniform sampler2D u_tex0;
uniform vec2 u_resolution;
uniform float u_time;
uniform float u_x0;
uniform float u_x1;
uniform float u_x2;

void main() {
    vec4 texColour = texture2D(u_tex0, v_texcoord);
    gl_FragColor = vec4(1.0 - u_x0 - texColour.r,1.0 -u_x1-texColour.g,1.0 - u_x2-texColour.b,texColour.a);
}
