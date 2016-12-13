%macro my_macro(ds);
    title "Printout of [&DS]";
    proc print data = &ds;
    run;
%mend;
