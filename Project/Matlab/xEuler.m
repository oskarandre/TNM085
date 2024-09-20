function [x,v,t] = xEuler(fun,tspan,v0,n,theta)

a = tspan(1);
b = tspan(2);
t = linspace(a,b,n+1);
h = t(2)-t(1);

x = zeros(1,n);
v = zeros(1,n);

v(1) = v0*cos(theta);

    for i = 1:n
        if v(i) + h*fun() <= 0
            v(i+1) = 0;
            x(i+1) = x(i);
        else
            v(i+1) = v(i) + h*fun();
            x(i+1) = x(i) + h*v(i+1);
        end    
    end
end