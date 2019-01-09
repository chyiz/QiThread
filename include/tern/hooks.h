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

/* Additional Modification by : Qi Zhao (qzhao6@ncsu.edu), Zhengyi Qiu (zqiu2@ncsu.edu), Guoliang Jin (guoliang_jin@ncsu.edu) */

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

/* Authors: Heming Cui (heming@cs.columbia.edu), Junfeng Yang (junfeng@cs.columbia.edu) -*- Mode: C++ -*- */


#ifndef __TERN_COMMON_HOOKS_H
#define __TERN_COMMON_HOOKS_H

/// hooks tern or developers insert to a multithreaded program.

#include <sys/time.h>
#include <sys/types.h>
#include <pthread.h>
#include <unistd.h>
#include <signal.h>
#include <semaphore.h>
#include <stdarg.h>


#ifdef __cplusplus
extern "C" {
#endif

  //  used by idle thread to skip empty rounds
  void tern_idle_sleep();
  void tern_idle_cond_wait();
  
  /// hooks that users insert translate into these
  void tern_symbolic_real(unsigned insid, void *addr,
                          int nbytes, const char *symname);
  void tern_dummy_sync_real();
  void tern_task_begin_real(unsigned insid, void *addr,
                            int nbytes, const char *name);
  void tern_task_end_real(unsigned insid);
  void tern_lineup_init_real(long opaque_type, unsigned count, unsigned timeout_turns);
  void tern_lineup_destroy_real(long opaque_type);
  void tern_lineup_start_real(long opaque_type);
  void tern_lineup_end_real(long opaque_type);
  void tern_non_det_start_real();
  void tern_non_det_end_real();
  void tern_set_slock_next_n(int next_n_turns);
  void tern_set_scwf_ignore_variable(int isSet);
  void tern_detach_real();
  void tern_non_det_barrier_end_real(int bar_id, int cnt);
  void tern_set_base_time_real(struct timespec *ts);

  /// hooks tern automatically inserts.  start with the ones tern provides
  void tern_prog_begin(void);   /// initializes tern internal data
  void tern_prog_end(void);     /// cleans up tern internal data
  void tern_thread_begin(void); /// called at the beginning of a thread
  void tern_thread_end(unsigned insid); /// called at the end of a thread

  /// print stat.
  void tern_print_runtime_stat();

  void tern___libc_start_main(void *func_ptr, int argc, char* argv[], void *init_func,
    void *fini_func, void *stack_end);   /// called in dynamic hook mode

  /// tern inserts these methods to a target program to make races
  /// deterministic; these methods are implemented only by the replayer
  void tern_fix_up();
  void tern_fix_down();

  /// now the hooks to synchronization methods and blocking system
  /// calls. add one extra argument, @insid or instruction ID to each hook
  /// to ease debugging.
# undef DEF
# undef DEFTERNAUTO
# undef DEFTERNUSER
# define DEF(func, kind, rettype, args...) \
    rettype tern_ ## func (unsigned insid, ##args);
# define DEFTERNAUTO(func)
# define DEFTERNUSER(func)
# include "syncfuncs.def.h"
# undef DEF
# undef DEFTERNAUTO
# undef DEFTERNUSER

#ifdef __cplusplus
}
#endif

#endif
