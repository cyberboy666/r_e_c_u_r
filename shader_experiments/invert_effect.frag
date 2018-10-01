

varying vec2 texcoord0;
uniform sampler2D tex0;
uniform vec2 u_resolution;
uniform float u_time;

void main() {
    vec4 texColour = texture2D(tex0, texcoord0);
    gl_FragColor = vec4(1.0-texColour.r,1.0-texColour.g,1.0-texColour.b,texColour.a);
}
