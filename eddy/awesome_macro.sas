%macro my_macro(ds);

    title "placeholder";
    footnote "A footnote";
    proc print data = &ds noobs;
    run;
    
%mend;
