%macro my_macro(ds);
    proc print data = &ds;
    run;
%mend;
