precision mediump float;
// template : glsl.ergonenous-tones.com

varying vec2 tcoord;    // location
uniform sampler2D tex;  // texture one
uniform sampler2D tex2; // texture two
uniform vec2 tres;      // size of texture (screen)
uniform vec4 fparams;   // 4 floats coming in
uniform ivec4 iparams;  // 4 ints coming in
uniform float ftime;    // 0.0 to 1.0
uniform int itime;      // increases when ftime hits 1.0
//f0::
//f1::
//f2::
float f0 = mix(0.0, 1.0, fparams[0]);
float f1 = mix(0.0, 1.0, fparams[1]);
float f2 = mix(0.0, 1.0, fparams[2]);

float time = float(itime) + ftime;
vec2 resolution = tres;

#define PI 3.1415926538979323846
#define TWO_PI 2*PI

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



vec4 displace(sampler2D tex, vec2 pos){
    vec4 texColourZoom;
    vec2 center;
    
    vec4 color = texture2D(tex, pos);
    vec3 hsv = rgb2hsv(color.rgb);
    float hueR = (floor(hsv.x*10.0)/10.0);
    float angle = (6.28 * hueR) + 6.28 * f1 ;
    float length = f2*0.05;

    if(hsv.z > 0.5){
    pos.x = pos.x + length* cos(angle);
    pos.y = pos.y + length* sin(angle);
	}
    if((pos.x < 0.0)||(pos.y < 0.0)||(pos.x > 1.0)||(pos.y > 1.0)){
        texColourZoom = vec4(0.0);
    }
    else{
        texColourZoom = texture2D(tex, pos);
    }
    return texColourZoom;
}

vec4 mixBlend(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    
    colour = texColour0;
    colour.xyz = (1.0 - f0) * texColour0.xyz + f0 * texColour1.xyz;

    return colour;
}

void main( void ) {
    vec4 texColour0;
    vec4 texColour1;

    texColour0 = texture2D(tex, tcoord);
    texColour1 = displace(tex2, tcoord);

    vec4 colour;


    colour = mixBlend(texColour0, texColour1);
    gl_FragColor = colour; 


//gl_FragColor = vec4(rgb, color.a);
}
