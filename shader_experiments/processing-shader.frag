// Created by inigo quilez - iq/2013
// License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.

uniform vec3      u_Resolution;           // viewport resolution (in pixels)
uniform float     u_Time;                 // shader playback time (in seconds)
uniform float     u_TimeDelta;            // render time (in seconds)
uniform int       u_Frame;                // shader playback frame
uniform float     u_ChannelTime[4];

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 q = fragCoord.xy / u_Resolution.xy;
    vec2 uv = 0.5 + (q-0.5)*(0.9 + 0.1*sin(0.2*u_Time));

    vec3 oricol = texture( u_Channel0, vec2(q.x,1.0-q.y) ).xyz;
    vec3 col;

    col.r = texture(u_Channel0,vec2(uv.x+0.003,-uv.y)).x;
    col.g = texture(u_Channel0,vec2(uv.x+0.000,-uv.y)).y;
    col.b = texture(u_Channel0,vec2(uv.x-0.003,-uv.y)).z;

    col = clamp(col*0.5+0.5*col*col*1.2,0.0,1.0);

    col *= 0.5 + 0.5*16.0*uv.x*uv.y*(1.0-uv.x)*(1.0-uv.y);

    col *= vec3(0.95,1.05,0.95);

    col *= 0.9+0.1*sin(10.0*u_Time+uv.y*1000.0);

    col *= 0.99+0.01*sin(110.0*u_Time);

    float comp = smoothstep( 0.2, 0.7, sin(u_Time) );
    col = mix( col, oricol, clamp(-2.0+2.0*q.x+3.0*comp,0.0,1.0) );

    fragColor = vec4(col,1.0);
}
