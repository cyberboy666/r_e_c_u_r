//1-input
//written by Tim Caldwell
#ifdef GL_ES
precision mediump float;
#endif

varying vec2 v_texcoord;
uniform sampler2D u_tex0;
uniform vec2 u_resolution;
uniform float u_time;
uniform float u_x0;

vec3 rgb2grayscale(vec3 c)
{
    return(vec3(dot(c, vec3(0.299, 0.587, 0.114))));
}

void main(){

vec2 pos = v_texcoord;
vec4 color = texture2D(u_tex0, pos);

vec3 gray = rgb2grayscale(color.rgb);

float divisions = 20.0 * u_x0 + 1.0;
vec3 newGray = vec3(float(int(gray.x*divisions))/divisions,float(int(gray.y*divisions))/divisions,float(int(gray.z*divisions))/divisions);

//if(gray.r + gray.g + gray.b )


gl_FragColor = vec4(newGray, color.a);

}





