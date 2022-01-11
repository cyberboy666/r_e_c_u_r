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


vec3 rgb2hsv(vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

vec4 mixBlendAdd0(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    
    vec3 hsvTexColour0 = rgb2hsv(texColour0.rgb);
    vec3 hsvTexColour1 = rgb2hsv(texColour1.rgb);

    if((1.0 - u_x0) * hsvTexColour0.z < u_x0 * hsvTexColour1.x){colour = texColour1;}
    else {colour = texColour0;}

    return colour;
}

vec4 mixBlendAdd1(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    
    vec3 hsvTexColour0 = rgb2hsv(texColour0.rgb);
    vec3 hsvTexColour1 = rgb2hsv(texColour1.rgb);

    if((1.0 - u_x0) * hsvTexColour0.z < u_x0  * hsvTexColour1.x){colour = texColour1;}
    else {colour = texColour0;}

    return colour;
}


void main() {

    vec2 pos = v_texcoord;
    vec4 texColour0;
    vec4 texColour1;

    texColour0 = texture2D(u_tex0, v_texcoord);
    texColour1 = texture2D(u_tex1, v_texcoord);


    vec4 colour;

    if(u_x1 > 0.5){colour = mixBlendAdd0(texColour0, texColour1);}
    else{colour = mixBlendAdd1(texColour0, texColour1);}

    gl_FragColor = colour; 

}
