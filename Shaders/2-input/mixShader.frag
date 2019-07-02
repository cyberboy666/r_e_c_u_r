//pro-shader
//written by Tim Caldwell
//this is a basic example of how to effect input textures position
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
uniform float u_x4;

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

vec4 mixVeritcalWipe(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    

    if(v_texcoord.x > u_x0){colour = texColour0;}
    else {colour = texColour1;}
    return colour;
}

vec4 mixHorizontalWipe(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    

    if(v_texcoord.y > u_x0){colour = texColour0;}
    else {colour = texColour1;}
    return colour;
}

vec4 mixLuma0(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    
    vec3 hsvTexColour0 = rgb2hsv(texColour0.rgb);

    if(hsvTexColour0.z > u_x0){colour = texColour0;}
    else {colour = texColour1;}
    return colour;
}

vec4 mixLuma1(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    
    vec3 hsvTexColour1 = rgb2hsv(texColour1.rgb);

    if(hsvTexColour1.z > u_x0){colour = texColour1;}
    else {colour = texColour0;}
    return colour;
}

vec4 mixBlend(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    
    colour = texColour0;
    colour.xyz = u_x0 * texColour0.xyz + (1.0 - u_x0) * texColour1.xyz;

    return colour;
}

vec4 mixBlendAdd(vec4 texColour0, vec4 texColour1) {
    vec4 colour;    
    vec3 hsvTexColour0 = rgb2hsv(texColour0.rgb);
    vec3 hsvTexColour1 = rgb2hsv(texColour1.rgb);

    if(u_x0 * hsvTexColour0.z < (1.0 - u_x0) * hsvTexColour1.x){colour = texColour1;}
    else {colour = texColour0;}

    return colour;
}

vec4 zoom(sampler2D tex, vec2 pos){
    vec4 texColourZoom;
    vec2 center;
    //center = vec2(u_x3 / u_resolution.x, u_x4 / u_resolution.y);
    center = vec2(u_x4, 0.5);

    pos.x = (pos.x - center.x)*(0.5 / u_x3) + center.x;
    pos.y = (pos.y - center.y)*(0.5 / u_x3) + center.y;
    if((pos.x < 0.0)||(pos.y < 0.0)||(pos.x > 1.0)||(pos.y > 1.0)){
        texColourZoom = vec4(0.0);
    }
    else{
        texColourZoom = texture2D(tex, pos);
    }
    return texColourZoom;
}

/* memory runs out when tryign this
vec4 rotate(sampler2D tex, vec2 pos){

    vec4 texColourRotate;
    vec2 center;
    //center = vec2(u_x3 / u_resolution.x, u_x4 / u_resolution.y);
    center = vec2(u_x4, 0.5);

    float r = distance(center, pos);
    float a = atan(pos.x - center.x, pos.y - center.y);

    pos.x = r * cos(a + 2.0 * 3.141592 * u_x3) + 0.5;
    pos.y = r * sin(a + 2.0 * 3.141592 * u_x3) + 0.5;
    
    if((pos.x < 0.0)||(pos.y < 0.0)||(pos.x > 1.0)||(pos.y > 1.0)){
        texColourRotate = vec4(0.0);
    }
    else{
        texColourRotate = texture2D(tex, pos);
    }
    return texColourRotate;
}
*/

void main() {

    vec2 pos = v_texcoord;
    vec4 texColour0;
    vec4 texColour1;

    if(0.2 <= u_x2 && u_x2 <= 0.4 ) {
        texColour0 = zoom(u_tex0, v_texcoord);
        texColour1 = zoom(u_tex1, v_texcoord);
        }
    //else if(0.6 <= u_x2 && u_x2 <= 0.8 ) {
        //texColour0 = rotate(u_tex0, v_texcoord);
        //texColour1 = rotate(u_tex1, v_texcoord);
        //}
    else{
        texColour0 = texture2D(u_tex0, v_texcoord);
        texColour1 = texture2D(u_tex1, v_texcoord);
        }


    vec4 colour;

    if(0.0 <= u_x1 && u_x1 <= 0.2 ) {colour = mixVeritcalWipe(texColour0, texColour1);}
    else if(0.2 <= u_x1 && u_x1 <= 0.4 ) {colour = mixLuma0(texColour0, texColour1);}
    else if(0.4 <= u_x1 && u_x1 <= 0.6 ) {colour = mixLuma1(texColour0, texColour1);}
    else if(0.6 <= u_x1 && u_x1 <= 0.8 ) {colour = mixBlend(texColour0, texColour1);}
    else if(0.8 <= u_x1 && u_x1 <= 1.0 ) {colour = mixBlendAdd(texColour0, texColour1);}


//hue and satuation displacement

    if(0.4 <= u_x2 && u_x2 <= 0.6 ) {
    vec3 hsv = rgb2hsv(colour.rgb);
    //hsv.x += u_x2 - 0.5;
    hsv.y = 2.0*u_x3* hsv.y;
    //hsv.z += u_x2 - 0.5;
    hsv.x = 2.0*u_x4* hsv.x;
    vec3 rgb = hsv2rgb(hsv.xyz);
    colour = vec4(rgb, colour.a);
        }
//---------





    gl_FragColor = colour; 

}


