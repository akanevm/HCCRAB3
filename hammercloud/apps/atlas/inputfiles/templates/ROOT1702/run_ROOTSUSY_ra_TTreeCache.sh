#!/bin/bash
export DCACHE_RAHEAD=TRUE
export DCACHE_RA_BUFFER=32768
unset DC_LOCAL_CACHE_BUFFER 


echo DCACHE SETTINGS
echo DCACHE_RAHEAD $DCACHE_RAHEAD
echo DC_LOCAL_CACHE_BUFFER $DC_LOCAL_CACHE_BUFFER
echo DC_LOCAL_CACHE_MEMORY_PER_FILE $DC_LOCAL_CACHE_MEMORY_PER_FILE
echo DC_LOCAL_CACHE_BLOCK_SIZE $DC_LOCAL_CACHE_BLOCK_SIZE
echo DCACHE_RA_BUFFER $DCACHE_RA_BUFFER

export LD_LIBRARY_PATH=/opt/misc/gridlab/demonstrators/dcap++.lib.d/:/opt/d-cache/dcap/lib:/opt/d-cache/dcap/lib64:$LD_LIBRARY_PATH
echo Setting LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH

root -l -b runGangaTTreeCache.C