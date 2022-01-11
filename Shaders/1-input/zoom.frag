//1-input
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

vec4 zoom(sampler2D tex, vec2 pos){
    vec4 texColourZoom;
    vec2 center;
    
    center = vec2(u_x2, u_x3);

    pos.x = (pos.x - center.x)*(0.5 / u_x0) + center.x;
    pos.y = (pos.y - center.y)*(0.5 / u_x0) + center.y;
    if((pos.x < 0.0)||(pos.y < 0.0)||(pos.x > 1.0)||(pos.y > 1.0)){
        texColourZoom = vec4(0.0);
    }
    else{
        texColourZoom = texture2D(tex, pos);
    }
    return texColourZoom;
}

void main(){

    vec2 pos = v_texcoord;
    vec4 texColour0;
    texColour0 = zoom(u_tex0, v_texcoord);

    gl_FragColor = texColour0; 

}





