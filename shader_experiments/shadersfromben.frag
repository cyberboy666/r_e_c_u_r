// Author:
// Title:

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

void main() {
    vec2 pos = gl_FragCoord.xy;
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    st.x *= u_resolution.x/u_resolution.y;
	
    /*float wave_length = 180.0;
    float period = 5.0;
    float speed = wave_length/period;
    float speed = 100.0;
    float period = wave_length/speed;
    float x_coef = 6.28/wave_length;
    float t_coef = 6.28/period;*/
    
    
    vec3 color = vec3(0.0,0.0,0.0);
    
    /*vec3 col1 = vec3(0.5, 0.0, 0.1);
    vec3 col2 = vec3(0.2, 0.1, 0.8);

    float mixer = sin(u_time);

    color = mix(col1, col2, mixer);*/

    // -------- Hypnotic circle thing ----------
    /*vec2 s1 = vec2(u_resolution.x*(0.5 + 0.25*cos(u_time)), u_resolution*(0.5 + 0.25*sin(u_time)));
    vec2 s2 = vec2(u_resolution.x*(0.5 + 0.25*sin(u_time)), u_resolution*(0.5 + 0.25*cos(u_time)));
    vec2 s3 = vec2(u_resolution.x*0.5, u_resolution*0.5);
    
    float r1 = pow(pow(pos.x-s1.x,2.0) + pow(pos.y-s1.y,2.0), 0.5);
    float r2 = pow(pow(pos.x-s2.x,2.0) + pow(pos.y-s2.y,2.0), 0.5);
    float r3 = pow(pow(pos.x-s3.x,2.0) + pow(pos.y-s3.y,2.0), 0.5);
    
    color += vec3(0.5 + 0.5*sign(sin((0.1 + 0.05*sin(u_time+2.0))*r1 - 1.0*u_time)), 0.0, 0.0);
    color += vec3(0.0, 0.0, 0.5 + 0.5*sign(sin((0.1 + 0.05*sin(u_time))*r2 - 1.2*u_time)));
    color += vec3(0.0, 0.5 + 0.5*sign(sin((0.1 + 0.05*sin(u_time+0.5))*r3 - 1.1*u_time)), 0.0);*/
    
    // ------- cool square wave thing ----------
    //color += vec3(sign(sin(0.05*pos.x - u_time + sin(0.05*pow(pos.y,1.5) - u_time))),0.,0.);
    //color += vec3(0., 0., sign(cos(0.03*pos.x - u_time + 0.5*sin(0.05*pos.y - u_time))));
    
    // ------- puff in puff out diamond --------
    color += vec3(sin(0.05*pos.x - cos(u_time)) + cos(0.05*pos.x/(0.1 + abs(cos(u_time/5.0)))),0.0,0.0);
    color += vec3(sin(0.05*pos.y - cos(u_time/5.0)) + cos(0.05*pos.y/(0.1 + abs(cos(u_time/5.0)))),0.0,0.0);
    color += vec3(0.0, 0.0, sin(u_time));
	//color = vec3(st.y);
 	
    
    
    gl_FragColor = vec4(color,1.);
}
