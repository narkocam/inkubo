@del enc_%1  /Q
@del %1.encoded /Q
@copy %1 %1.original
@python py-to-marshall.py %1
@del tmp_%1 /Q
@ren enc_%1 %1.encoded



