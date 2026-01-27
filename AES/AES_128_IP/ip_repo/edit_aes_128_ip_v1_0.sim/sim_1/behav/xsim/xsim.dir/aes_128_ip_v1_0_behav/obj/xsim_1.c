/**********************************************************************/
/*   ____  ____                                                       */
/*  /   /\/   /                                                       */
/* /___/  \  /                                                        */
/* \   \   \/                                                         */
/*  \   \        Copyright (c) 2003-2013 Xilinx, Inc.                 */
/*  /   /        All Right Reserved.                                  */
/* /---/   /\                                                         */
/* \   \  /  \                                                        */
/*  \___\/\___\                                                       */
/**********************************************************************/


#include "iki.h"
#include <string.h>
#include <math.h>
#ifdef __GNUC__
#include <stdlib.h>
#else
#include <malloc.h>
#define alloca _alloca
#endif
/**********************************************************************/
/*   ____  ____                                                       */
/*  /   /\/   /                                                       */
/* /___/  \  /                                                        */
/* \   \   \/                                                         */
/*  \   \        Copyright (c) 2003-2013 Xilinx, Inc.                 */
/*  /   /        All Right Reserved.                                  */
/* /---/   /\                                                         */
/* \   \  /  \                                                        */
/*  \___\/\___\                                                       */
/**********************************************************************/


#include "iki.h"
#include <string.h>
#include <math.h>
#ifdef __GNUC__
#include <stdlib.h>
#else
#include <malloc.h>
#define alloca _alloca
#endif
typedef void (*funcp)(char *, char *);
extern int main(int, char**);
extern void execute_3(char*, char *);
extern void execute_4(char*, char *);
extern void execute_5(char*, char *);
extern void execute_6(char*, char *);
extern void execute_7(char*, char *);
extern void execute_8(char*, char *);
extern void execute_9(char*, char *);
extern void execute_10(char*, char *);
extern void execute_11(char*, char *);
extern void vlog_simple_process_execute_0_fast_no_reg_no_agg(char*, char*, char*);
extern void execute_958(char*, char *);
extern void execute_959(char*, char *);
extern void execute_1819(char*, char *);
extern void execute_1820(char*, char *);
extern void execute_13(char*, char *);
extern void execute_1788(char*, char *);
extern void execute_1789(char*, char *);
extern void execute_1790(char*, char *);
extern void execute_1791(char*, char *);
extern void execute_1792(char*, char *);
extern void execute_1793(char*, char *);
extern void execute_1794(char*, char *);
extern void execute_1795(char*, char *);
extern void execute_1796(char*, char *);
extern void execute_1797(char*, char *);
extern void execute_1798(char*, char *);
extern void execute_1799(char*, char *);
extern void execute_1800(char*, char *);
extern void execute_1801(char*, char *);
extern void execute_1802(char*, char *);
extern void execute_1803(char*, char *);
extern void execute_1804(char*, char *);
extern void execute_1805(char*, char *);
extern void execute_1806(char*, char *);
extern void execute_1807(char*, char *);
extern void execute_1808(char*, char *);
extern void execute_1809(char*, char *);
extern void execute_1810(char*, char *);
extern void execute_1811(char*, char *);
extern void execute_1812(char*, char *);
extern void execute_1813(char*, char *);
extern void execute_1814(char*, char *);
extern void execute_1815(char*, char *);
extern void execute_1816(char*, char *);
extern void execute_1817(char*, char *);
extern void execute_1818(char*, char *);
extern void execute_15(char*, char *);
extern void execute_25(char*, char *);
extern void execute_960(char*, char *);
extern void execute_961(char*, char *);
extern void execute_962(char*, char *);
extern void execute_963(char*, char *);
extern void execute_964(char*, char *);
extern void execute_969(char*, char *);
extern void execute_970(char*, char *);
extern void execute_971(char*, char *);
extern void execute_972(char*, char *);
extern void execute_973(char*, char *);
extern void execute_965(char*, char *);
extern void execute_966(char*, char *);
extern void execute_967(char*, char *);
extern void execute_968(char*, char *);
extern void execute_18(char*, char *);
extern void execute_219(char*, char *);
extern void execute_1100(char*, char *);
extern void execute_1101(char*, char *);
extern void execute_1170(char*, char *);
extern void execute_1171(char*, char *);
extern void execute_1172(char*, char *);
extern void execute_1173(char*, char *);
extern void execute_1102(char*, char *);
extern void execute_1103(char*, char *);
extern void execute_1104(char*, char *);
extern void execute_1105(char*, char *);
extern void execute_1106(char*, char *);
extern void execute_140(char*, char *);
extern void execute_945(char*, char *);
extern void execute_1766(char*, char *);
extern void execute_1767(char*, char *);
extern void execute_1784(char*, char *);
extern void execute_1785(char*, char *);
extern void execute_1786(char*, char *);
extern void execute_1787(char*, char *);
extern void execute_947(char*, char *);
extern void execute_948(char*, char *);
extern void execute_949(char*, char *);
extern void execute_1821(char*, char *);
extern void execute_1822(char*, char *);
extern void execute_1823(char*, char *);
extern void execute_1824(char*, char *);
extern void execute_1825(char*, char *);
extern void vlog_transfunc_eventcallback(char*, char*, unsigned, unsigned, unsigned, char *);
extern void transaction_100(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_123(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_146(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_169(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_192(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_215(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_238(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_261(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_284(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_307(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_336(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_337(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_338(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_340(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_341(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_342(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_344(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_345(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_346(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_348(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_349(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_350(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_425(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_426(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_427(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_429(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_430(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_431(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_433(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_434(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_435(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_437(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_438(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_439(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_514(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_515(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_516(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_518(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_519(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_520(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_522(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_523(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_524(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_526(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_527(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_528(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_603(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_604(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_605(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_607(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_608(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_609(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_611(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_612(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_613(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_615(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_616(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_617(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_692(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_693(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_694(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_696(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_697(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_698(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_700(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_701(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_702(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_704(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_705(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_706(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_781(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_782(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_783(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_785(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_786(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_787(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_789(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_790(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_791(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_793(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_794(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_795(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_870(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_871(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_872(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_874(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_875(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_876(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_878(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_879(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_880(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_882(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_883(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_884(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_959(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_960(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_961(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_963(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_964(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_965(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_967(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_968(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_969(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_971(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_972(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_973(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1048(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1049(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1050(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1052(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1053(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1054(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1056(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1057(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1058(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1060(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1061(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1062(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1141(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1142(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1143(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1144(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1145(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1146(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1147(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1148(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1149(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1150(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1151(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1152(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1153(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1154(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1155(char*, char*, unsigned, unsigned, unsigned);
extern void transaction_1156(char*, char*, unsigned, unsigned, unsigned);
funcp funcTab[226] = {(funcp)execute_3, (funcp)execute_4, (funcp)execute_5, (funcp)execute_6, (funcp)execute_7, (funcp)execute_8, (funcp)execute_9, (funcp)execute_10, (funcp)execute_11, (funcp)vlog_simple_process_execute_0_fast_no_reg_no_agg, (funcp)execute_958, (funcp)execute_959, (funcp)execute_1819, (funcp)execute_1820, (funcp)execute_13, (funcp)execute_1788, (funcp)execute_1789, (funcp)execute_1790, (funcp)execute_1791, (funcp)execute_1792, (funcp)execute_1793, (funcp)execute_1794, (funcp)execute_1795, (funcp)execute_1796, (funcp)execute_1797, (funcp)execute_1798, (funcp)execute_1799, (funcp)execute_1800, (funcp)execute_1801, (funcp)execute_1802, (funcp)execute_1803, (funcp)execute_1804, (funcp)execute_1805, (funcp)execute_1806, (funcp)execute_1807, (funcp)execute_1808, (funcp)execute_1809, (funcp)execute_1810, (funcp)execute_1811, (funcp)execute_1812, (funcp)execute_1813, (funcp)execute_1814, (funcp)execute_1815, (funcp)execute_1816, (funcp)execute_1817, (funcp)execute_1818, (funcp)execute_15, (funcp)execute_25, (funcp)execute_960, (funcp)execute_961, (funcp)execute_962, (funcp)execute_963, (funcp)execute_964, (funcp)execute_969, (funcp)execute_970, (funcp)execute_971, (funcp)execute_972, (funcp)execute_973, (funcp)execute_965, (funcp)execute_966, (funcp)execute_967, (funcp)execute_968, (funcp)execute_18, (funcp)execute_219, (funcp)execute_1100, (funcp)execute_1101, (funcp)execute_1170, (funcp)execute_1171, (funcp)execute_1172, (funcp)execute_1173, (funcp)execute_1102, (funcp)execute_1103, (funcp)execute_1104, (funcp)execute_1105, (funcp)execute_1106, (funcp)execute_140, (funcp)execute_945, (funcp)execute_1766, (funcp)execute_1767, (funcp)execute_1784, (funcp)execute_1785, (funcp)execute_1786, (funcp)execute_1787, (funcp)execute_947, (funcp)execute_948, (funcp)execute_949, (funcp)execute_1821, (funcp)execute_1822, (funcp)execute_1823, (funcp)execute_1824, (funcp)execute_1825, (funcp)vlog_transfunc_eventcallback, (funcp)transaction_100, (funcp)transaction_123, (funcp)transaction_146, (funcp)transaction_169, (funcp)transaction_192, (funcp)transaction_215, (funcp)transaction_238, (funcp)transaction_261, (funcp)transaction_284, (funcp)transaction_307, (funcp)transaction_336, (funcp)transaction_337, (funcp)transaction_338, (funcp)transaction_340, (funcp)transaction_341, (funcp)transaction_342, (funcp)transaction_344, (funcp)transaction_345, (funcp)transaction_346, (funcp)transaction_348, (funcp)transaction_349, (funcp)transaction_350, (funcp)transaction_425, (funcp)transaction_426, (funcp)transaction_427, (funcp)transaction_429, (funcp)transaction_430, (funcp)transaction_431, (funcp)transaction_433, (funcp)transaction_434, (funcp)transaction_435, (funcp)transaction_437, (funcp)transaction_438, (funcp)transaction_439, (funcp)transaction_514, (funcp)transaction_515, (funcp)transaction_516, (funcp)transaction_518, (funcp)transaction_519, (funcp)transaction_520, (funcp)transaction_522, (funcp)transaction_523, (funcp)transaction_524, (funcp)transaction_526, (funcp)transaction_527, (funcp)transaction_528, (funcp)transaction_603, (funcp)transaction_604, (funcp)transaction_605, (funcp)transaction_607, (funcp)transaction_608, (funcp)transaction_609, (funcp)transaction_611, (funcp)transaction_612, (funcp)transaction_613, (funcp)transaction_615, (funcp)transaction_616, (funcp)transaction_617, (funcp)transaction_692, (funcp)transaction_693, (funcp)transaction_694, (funcp)transaction_696, (funcp)transaction_697, (funcp)transaction_698, (funcp)transaction_700, (funcp)transaction_701, (funcp)transaction_702, (funcp)transaction_704, (funcp)transaction_705, (funcp)transaction_706, (funcp)transaction_781, (funcp)transaction_782, (funcp)transaction_783, (funcp)transaction_785, (funcp)transaction_786, (funcp)transaction_787, (funcp)transaction_789, (funcp)transaction_790, (funcp)transaction_791, (funcp)transaction_793, (funcp)transaction_794, (funcp)transaction_795, (funcp)transaction_870, (funcp)transaction_871, (funcp)transaction_872, (funcp)transaction_874, (funcp)transaction_875, (funcp)transaction_876, (funcp)transaction_878, (funcp)transaction_879, (funcp)transaction_880, (funcp)transaction_882, (funcp)transaction_883, (funcp)transaction_884, (funcp)transaction_959, (funcp)transaction_960, (funcp)transaction_961, (funcp)transaction_963, (funcp)transaction_964, (funcp)transaction_965, (funcp)transaction_967, (funcp)transaction_968, (funcp)transaction_969, (funcp)transaction_971, (funcp)transaction_972, (funcp)transaction_973, (funcp)transaction_1048, (funcp)transaction_1049, (funcp)transaction_1050, (funcp)transaction_1052, (funcp)transaction_1053, (funcp)transaction_1054, (funcp)transaction_1056, (funcp)transaction_1057, (funcp)transaction_1058, (funcp)transaction_1060, (funcp)transaction_1061, (funcp)transaction_1062, (funcp)transaction_1141, (funcp)transaction_1142, (funcp)transaction_1143, (funcp)transaction_1144, (funcp)transaction_1145, (funcp)transaction_1146, (funcp)transaction_1147, (funcp)transaction_1148, (funcp)transaction_1149, (funcp)transaction_1150, (funcp)transaction_1151, (funcp)transaction_1152, (funcp)transaction_1153, (funcp)transaction_1154, (funcp)transaction_1155, (funcp)transaction_1156};
const int NumRelocateId= 226;

void relocate(char *dp)
{
	iki_relocate(dp, "xsim.dir/aes_128_ip_v1_0_behav/xsim.reloc",  (void **)funcTab, 226);

	/*Populate the transaction function pointer field in the whole net structure */
}

void sensitize(char *dp)
{
	iki_sensitize(dp, "xsim.dir/aes_128_ip_v1_0_behav/xsim.reloc");
}

void simulate(char *dp)
{
	iki_schedule_processes_at_time_zero(dp, "xsim.dir/aes_128_ip_v1_0_behav/xsim.reloc");
	// Initialize Verilog nets in mixed simulation, for the cases when the value at time 0 should be propagated from the mixed language Vhdl net
	iki_execute_processes();

	// Schedule resolution functions for the multiply driven Verilog nets that have strength
	// Schedule transaction functions for the singly driven Verilog nets that have strength

}
#include "iki_bridge.h"
void relocate(char *);

void sensitize(char *);

void simulate(char *);

int main(int argc, char **argv)
{
    iki_heap_initialize("ms", "isimmm", 0, 2147483648) ;
    iki_set_sv_type_file_path_name("xsim.dir/aes_128_ip_v1_0_behav/xsim.svtype");
    iki_set_crvs_dump_file_path_name("xsim.dir/aes_128_ip_v1_0_behav/xsim.crvsdump");
    void* design_handle = iki_create_design("xsim.dir/aes_128_ip_v1_0_behav/xsim.mem", (void *)relocate, (void *)sensitize, (void *)simulate, 0, isimBridge_getWdbWriter(), 0, argc, argv);
     iki_set_rc_trial_count(100);
    (void) design_handle;
    return iki_simulate_design();
}
