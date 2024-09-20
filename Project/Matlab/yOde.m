function [dy] = yOde(pos,a)

    g = 9.8;
    m = 0.25;
    fk = 0.07;
    c = 1/5;


    if pos >= 0
       dy = m*(a - c*exp(pos)*g*fk);
    else
       dy = m*(a + c*exp(pos)*g*fk);
    end
end