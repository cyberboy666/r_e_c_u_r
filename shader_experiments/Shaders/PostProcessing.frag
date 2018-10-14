precision highp float;

uniform vec2 u_resolution;
uniform float u_time;
uniform sampler2D u_tex0;


// http://www.iquilezles.org/apps/shadertoy/?p=Postpro		
void main(){
	vec2 q = gl_FragCoord.xy / u_resolution.xy;
    vec2 uv = 0.5 + (q-0.5)*(0.9 + 0.1*sin(0.2*u_time));

    vec3 oricol = texture2D(u_tex0,vec2(q.x,1.0-q.y)).xyz;
    vec3 col;

    col.r = texture2D(u_tex0,vec2(uv.x+0.003,-uv.y)).x;
    col.g = texture2D(u_tex0,vec2(uv.x+0.000,-uv.y)).y;
    col.b = texture2D(u_tex0,vec2(uv.x-0.003,-uv.y)).z;

    col = clamp(col*0.5+0.5*col*col*1.2,0.0,1.0);

    col *= 0.5 + 0.5*16.0*uv.x*uv.y*(1.0-uv.x)*(1.0-uv.y);

    col *= vec3(0.8,1.0,0.7);

    col *= 0.9+0.1*sin(10.0*u_time+uv.y*1000.0);

    col *= 0.97+0.03*sin(110.0*u_time);

    float comp = smoothstep( 0.2, 0.7, sin(u_time) );
    col = mix( col, oricol, clamp(-2.0+2.0*q.x+3.0*comp,0.0,1.0) );

    gl_FragColor = vec4(col,1.0);
}
