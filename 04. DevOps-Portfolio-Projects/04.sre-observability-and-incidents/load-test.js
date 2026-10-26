import http from 'k6/http';
import {check,sleep} from 'k6';
export const options={vus:Number(__ENV.VUS||5),duration:__ENV.DURATION||'60s',thresholds:{http_req_failed:['rate<0.01'],http_req_duration:['p(95)<500']}};
export default function(){const response=http.post(__ENV.URL||'http://127.0.0.1:8080/checkout',JSON.stringify({item:'portfolio-book'}),{headers:{'Content-Type':'application/json'}});check(response,{'checkout accepted':r=>r.status===201});sleep(.2);}
