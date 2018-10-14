// copied from http://glslsandbox.com/e#47821.0
//gen-shader
#ifdef GL_ES
precision mediump float;
#endif

#extension GL_OES_standard_derivatives : enable

uniform float u_time;
uniform float u_x0;
uniform float u_x1;
uniform vec2 u_resolution;

void main( void ) {

	vec2 position = ( gl_FragCoord.xy / u_resolution.xy ) + (u_resolution.x * u_x0, u_resolution.y * u_x1) / 4.0;

	float color = 0.0;
	color += sin( position.x * cos( u_time / 15.0 ) * 80.0 ) + cos( position.y * cos( u_time / 15.0 ) * 10.0 );
	color += sin( position.y * sin( u_time / 10.0 ) * 40.0 ) + cos( position.x * sin( u_time / 25.0 ) * 40.0 );
	color += sin( position.x * sin( u_time / 5.0 ) * 10.0 ) + sin( position.y * sin( u_time / 35.0 ) * 80.0 );
	color *= sin( u_time / 10.0 ) * 0.8;

	gl_FragColor = vec4( vec3( color, color * 0.5, sin( color + u_time / 3.0 ) * 0.75 ), 1.0 );
}
