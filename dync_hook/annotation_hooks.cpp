/* Additional Modification Copyright (c) 2016-2018 North Carolina State University.
 * All rights reserved.
 * Redistribution and use in source and binary forms, with or without 
 * modification, are permitted provided that the following conditions are met:
 * 
 * 1. Redistributions and use are permitted for internal research purposes only, 
 * and commercial use is strictly prohibited under this license. Inquiries 
 * regarding commercial use should be directed to the Office of Technology 
 * Transfer at North Carolina State University, 919‐515‐7199, https://research.
 * ncsu.edu/otcnv/contact/, techtransfer@ncsu.edu.
 * 
 * 2. Commercial use means the sale, lease, export, transfer, conveyance or other 
 * distribution to a third party for financial gain, income generation or other 
 * commercial purposes of any kind, whether direct or indirect. Commercial use 
 * also means providing a service to a third party for financial gain, income 
 * generation or other commercial purposes of any kind, whether direct or 
 * indirect.
 * 
 * 3. Redistributions of source code must retain the above copyright notice, this 
 * list of conditions and the following disclaimer.
 * 
 * 4. Redistributions in binary form must reproduce the above copyright notice, 
 * this list of conditions and the following disclaimer in the documentation and/
 * or other materials provided with the distribution.
 * 
 * 5. The names “North Carolina State University”, “NCSU” and any trade‐name,
 * personal name, trademark, trade device, service mark, symbol, image, icon, or 
 * any abbreviation, contraction or simulation thereof owned by North Carolina 
 * State University must not be used to endorse or promote products derived from 
 * this software without prior written permission. For written permission, please
 * contact trademarks@ncsu.edu.
 * 
 * Disclaimer: THIS SOFTWARE IS PROVIDED “AS IS” AND ANY EXPRESSED OR IMPLIED 
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
 * EVENT SHALL THE APACHE SOFTWARE FOUNDATION OR ITS CONTRIBUTORS BE LIABLE FOR 
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (
 * INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
 */

/* Copyright (c) 2013,  Regents of the Columbia University 
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other 
 * materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
 * IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef __SPEC_HOOK_tern_lineup_init
extern "C" void soba_init(long opaque_type, unsigned count, unsigned timeout_turns){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && !options::disable_soba) {
    tern_lineup_init_real(opaque_type, count, timeout_turns);
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_lineup_destroy
extern "C" void soba_destroy(long opaque_type){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && !options::disable_soba) {
    tern_lineup_destroy_real(opaque_type);
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_lineup_start
extern "C" void tern_lineup_start(long opaque_type){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && !options::disable_soba) {
    tern_lineup_start_real(opaque_type);
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_lineup_end
extern "C" void tern_lineup_end(long opaque_type){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && !options::disable_soba) {
    tern_lineup_end_real(opaque_type);
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_lineup
extern "C" void soba_wait(long opaque_type){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && !options::disable_soba) {
    tern_lineup_start_real(opaque_type);
    tern_lineup_end_real(opaque_type);
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_non_det_start
extern "C" void pcs_enter(){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && options::enforce_non_det_annotations) {
    tern_non_det_start_real();
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_non_det_end
extern "C" void pcs_exit(){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && options::enforce_non_det_annotations) {
    tern_non_det_end_real();
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_next_n
extern "C" void slock_next_n(int next_n_turns){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && options::enforce_next_n_annotations) {
    tern_set_slock_next_n(next_n_turns);
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_next_n
extern "C" void scwf_ignore_variable(int isSet){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations) {
    tern_set_scwf_ignore_variable(isSet);
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif


#ifndef __SPEC_HOOK_tern_dummy_sync
extern "C" void tern_dummy_sync(){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && options::enforce_dummy_sync) {
    tern_dummy_sync_real();
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_set_base_time
extern "C" void tern_set_base_timespec(struct timespec *ts){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations) {
    tern_set_base_time_real(ts);
  } 
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_set_base_time
extern "C" void tern_set_base_timeval(struct timeval *tv){
#ifdef __USE_TERN_RUNTIME
  struct timespec ts;
  ts.tv_sec = tv->tv_sec;
  ts.tv_nsec = tv->tv_usec * 1000;
  if (Space::isApp() && options::DMT && options::enforce_annotations) {
    tern_set_base_time_real(&ts);
  }
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_detach
extern "C" void tern_detach(){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations) {
    tern_detach_real();
  }
#endif
  // If not runnning with xtern, NOP.
}
#endif

#ifndef __SPEC_HOOK_tern_non_det_barrier_end
extern "C" void pcs_barrier_exit(int bar_id, int cnt){
#ifdef __USE_TERN_RUNTIME
  if (Space::isApp() && options::DMT && options::enforce_annotations && options::enforce_non_det_annotations) {
    tern_non_det_barrier_end_real(bar_id, cnt);
  }
#endif
  // If not runnning with xtern, NOP.
}
#endif
