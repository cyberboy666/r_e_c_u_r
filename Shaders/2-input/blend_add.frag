//2-input
#ifdef GL_ES
precision mediump float;
#endif

varying vec2 v_texcoord;
uniform sampler2D u_tex0;
uniform sampler2D u_tex1;
uniform vec2 u_resolution;
uniform float u_time;
uniform float u_x0;
uniform float u_x1;
uniform float u_x2;
uniform float u_x3;

vec4 mixBlend(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    
    colour = texColour0;
    colour.xyz = (1.0 - u_x0) * texColour0.xyz + u_x0 * texColour1.xyz;

    return colour;
}


void main() {

    vec2 pos = v_texcoord;
    vec4 texColour0;
    vec4 texColour1;

    texColour0 = texture2D(u_tex0, v_texcoord);
    texColour1 = texture2D(u_tex1, v_texcoord);


    vec4 colour;


    colour = mixBlend(texColour0, texColour1);

    gl_FragColor = colour; 

}
