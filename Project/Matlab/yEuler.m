function [y,v,t] = yEuler(fun,tspan,y0,v0,n,theta)
    
    a = tspan(1);
    b = tspan(2);
    t = linspace(a,b,n+1);
    h = t(2)-t(1);
    
    y = zeros(1,n+1);
    v = zeros(1,n+1);
    
    y(1) = y0;
    v(1) = v0*sin(theta);

    for i = 1:n
        pos = y(i);

        if i == 1
            v(i+1) = v(i) + h*fun(pos,0);
        else
            v(i+1) = v(i) + h*fun(pos,v(i)-v(i-1)); %v(i)-v(i-1) = accelerationen
        end
%         v(i+1) = v(i) + h*fun(pos,v(i));
        y(i+1) = y(i)+ h*v(i+1);
    end

end