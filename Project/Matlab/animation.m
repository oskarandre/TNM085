function null = animation(x,y)

[d1,d2] = drawField();
plot(d1,d2);
hold on
for i = 1:length(x)
    h = plot(y(i),x(i),'o r');            % draw something on the trajectory
    axis([-1 1 0 8])
    pause(0.01)                                % wait a minute
    delete(h)                                 % delete it
end

end