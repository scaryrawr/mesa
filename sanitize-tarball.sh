#!/bin/sh
#
# usage: sanitize-tarball.sh [tarball]

dirname=$(basename $(basename "$1" .tar.bz2) .tar.xz)

tar xf "$1"
pushd $dirname

cat > src/gallium/auxiliary/vl/vl_mpeg12_decoder.c << EOF
#include "vl_mpeg12_decoder.h"
struct pipe_video_decoder *
vl_create_mpeg12_decoder(struct pipe_context *context,
                         enum pipe_video_profile profile,
			 enum pipe_video_entrypoint entrypoint,
			 enum pipe_video_chroma_format chroma_format,
			 unsigned width, unsigned height,
			 unsigned max_references,
			 bool expect_chunked_decode)
{
    return NULL;
}
EOF

cat > src/gallium/auxiliary/vl/vl_decoder.c << EOF
#include "vl_decoder.h"
bool vl_profile_supported(struct pipe_screen *screen,
                          enum pipe_video_profile profile)
{
    return false;
}
struct pipe_video_decoder *
vl_create_decoder(struct pipe_context *pipe,
                  enum pipe_video_profile profile,
                  enum pipe_video_entrypoint entrypoint,
                  enum pipe_video_chroma_format chroma_format,
                  unsigned width, unsigned height, unsigned max_references,
                  bool expect_chunked_decode)
{
    return NULL;
}
EOF

popd
tar Jcf $dirname.tar.xz $dirname
