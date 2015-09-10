#include "lfsr.h"

// standard seed
#define LFSR_SEED  ( 0x6A )

// bit-sliced seed
#define LFSR_SEED0 ( 0x0  )
#define LFSR_SEED1 ( 0x1  )
#define LFSR_SEED2 ( 0x0  )
#define LFSR_SEED3 ( 0x1  )
#define LFSR_SEED4 ( 0x0  )
#define LFSR_SEED5 ( 0x1  )
#define LFSR_SEED6 ( 0x1  )
#define LFSR_SEED7 ( 0x0  )

#if defined( LFSR_OPTION_1 )
// standard 8-bit state register
uint8_t S = LFSR_SEED;
                                                                               
uint8_t lfsr() {
  // extract output bit
  uint8_t r  = S & 1;
  // compute new bit
  uint8_t t  = ( S >> 0 ) ^
               ( S >> 4 ) ^
               ( S >> 5 ) ^
               ( S >> 6 ) ;
  // update register
          S  = ( S >> 1 ) ;
          S |= ( t << 7 ) ;
  // return result
  return r;
}
#endif      
                     
#if defined( LFSR_OPTION_2 )
// bit-sliced state register: S[i] is i-th slice,
// i.e.., i-th bit, of state
uint8_t S[ 8 ] = { LFSR_SEED0, LFSR_SEED1,
                   LFSR_SEED2, LFSR_SEED3,
                   LFSR_SEED4, LFSR_SEED5,
                   LFSR_SEED6, LFSR_SEED7 };

uint8_t lfsr() {
  // extract output bit
  uint8_t r = S[ 0 ] ;
  // compute new bit
  uint8_t t = S[ 0 ] ^
              S[ 4 ] ^
              S[ 5 ] ^
              S[ 6 ] ;
  // update register
  S[ 0 ] = S[ 1 ];
  S[ 1 ] = S[ 2 ];
  S[ 2 ] = S[ 3 ];
  S[ 3 ] = S[ 4 ];
  S[ 4 ] = S[ 5 ];
  S[ 5 ] = S[ 6 ];
  S[ 6 ] = S[ 7 ];                                                             
  S[ 7 ] = t     ;
  // return result                                                                               
  return r;
}
#endif

int main( int argc, char* argv[] ) {
  for( int i = 0; i < 32; i++ ) {
    printf( "i=%2d, lfsr output = %d\n", i, lfsr() & 1 );
  }

  return 0;
}

