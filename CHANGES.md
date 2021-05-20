# Changes

## 0.7.0
*2021-05-20*

* Upgrade `wps-tools` to `2.0.0`

## 0.6.1
*2021-05-04*

* Pin stable version of `wps-tools`

## 0.6.0
*2021-03-25*

* Handle multiple inputs

## 0.5.0
*2021-02-08*

* Add `wps_tools.output_handling` to demos
* Add `ProcessError`s
* Use `csv` content as input instead of file
* Add `Rds` file handling

## 0.4.2
*2020-12-24*

* Optimize Docker build

## 0.4.1
*2020-12-23*

* Update default target port

## 0.4.0
*2020-12-14*

* Create wps_climdex_spells with climdex.wsdi(#[51](https://github.com/pacificclimate/quail/pull/51))
* Create wps_climdexInput_csv(#[52](https://github.com/pacificclimate/quail/pull/52))
* Add climdex.csdi to wps_climdex_spells(#[53](https://github.com/pacificclimate/quail/pull/53))
* Create wps_climdex_temp_pctl with climdex.tn10p(#[54](https://github.com/pacificclimate/quail/pull/54))
* Add climdex.cdd to wps_climdex_spells(#[55](https://github.com/pacificclimate/quail/pull/55))
* Add climdex.cwd to wps_climdex_spells(#[56](https://github.com/pacificclimate/quail/pull/56))
* Add climdex.tn90p to wps_climdex_temp_pctl(#[57](https://github.com/pacificclimate/quail/pull/57))
* Create wps_climdex_rmm with climdex.r10mm, climdex.r20mm, and climdex.rnnmm(#[58](https://github.com/pacificclimate/quail/pull/58))
* Add tx10p option to wps_climdex_temp_pctl(#[59](https://github.com/pacificclimate/quail/pull/59))
* Add tx90p option to wps_climdex_temp_pctl(#[60](https://github.com/pacificclimate/quail/pull/60))53
* Create wps_climdex_dtr(#[61](https://github.com/pacificclimate/quail/pull/61))
* Create wps_climdex_ptot(#[62](https://github.com/pacificclimate/quail/pull/62))
* Add r99ptot to wps_climdex_ptot(#[63](https://github.com/pacificclimate/quail/pull/63))
* Create wps_climdex_sdii(#[64](https://github.com/pacificclimate/quail/pull/64))
* Create wps_climdex_rxnday with climdex.rx1day(#[65](https://github.com/pacificclimate/quail/pull/65))
* Create wps_climdex_quantile(#[66](https://github.com/pacificclimate/quail/pull/66))
* Add climdex.rx5day to wps_climdex_rxnday(#[67](https://github.com/pacificclimate/quail/pull/67))
* Create wps_climdex_get_available_indices(#[69](https://github.com/pacificclimate/quail/pull/69))
* Add climdex.prcptot to wps_climdex_ptot(#[70](https://github.com/pacificclimate/quail/pull/70))

## 0.3.0
*2020-12-09*

* Create wps_climdex_mmdmt with climdex.txx(#[42](https://github.com/pacificclimate/quail/pull/42))
* Add climdex.tnx to wps_climdex_mmdmt(#[44](https://github.com/pacificclimate/quail/pull/44))
* Add climdex.txn to wps_climdex_mmdmt(#[46](https://github.com/pacificclimate/quail/pull/46))
* Create wps_climdexInput_raw(#[49](https://github.com/pacificclimate/quail/pull/49))
* Add climdex.tnn to wps_climdex_mmdmt(#[50](https://github.com/pacificclimate/quail/pull/50))

## 0.2.0
*2020-12-04*

* Add summer days process (#[36](https://github.com/pacificclimate/quail/pull/36))
* Add frost days to wps_climdex_days process (#[37](https://github.com/pacificclimate/quail/pull/37))
* Add icing days to wps_climdex_days process (#[38](https://github.com/pacificclimate/quail/pull/38))
* Add wps_climdex_gsl process (#[40](https://github.com/pacificclimate/quail/pull/40))
* Add tropical nights to wps_climdex_days process (#[41](https://github.com/pacificclimate/quail/pull/41))

## 0.1.0
*2020-11-24*

* Add github workflows (#[1](https://github.com/pacificclimate/quail/pull/1)
* Add pavics-component (#[2](https://github.com/pacificclimate/quail/pull/2)
* Update ``docker-compose.yml`` for work on ``dev03`` (#[3](https://github.com/pacificclimate/quail/pull/3)
* Rework ``Dockerfile`` (#[4](https://github.com/pacificclimate/quail/pull/4)
* Update ``Makefile`` commands (#[5](https://github.com/pacificclimate/quail/pull/5)
