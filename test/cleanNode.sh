ssh -T -n -f song0254@csel-kh1250-05.cselabs.umn.edu  'pkill -f ".*python3 computeNode.py 0.*"' -U song0254
ssh -T -n -f song0254@csel-kh1250-07.cselabs.umn.edu  'pkill -f ".*python3 computeNode.py 1.*"' -U song0254
ssh -T -n -f song0254@csel-kh1250-08.cselabs.umn.edu  'pkill -f ".*python3 computeNode.py 2.*"' -U song0254
ssh -T -n -f song0254@csel-kh1250-09.cselabs.umn.edu  'pkill -f ".*python3 computeNode.py 3.*"' -U song0254
