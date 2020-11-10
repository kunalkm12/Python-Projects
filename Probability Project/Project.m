clear
load('data_EAS595.mat')

%%%%% Step 1: Training
mean1 = [0 0 0 0 0];
mean2 = [0 0 0 0 0];
for i = 1:5
    for j = 1:100
        mean1(i) = mean1(i) + F1(j,i);
        mean2(i) = mean2(i) + F2(j,i);
    end
end
for i = 1:5
    mean1(i) = mean1(i)/100;
    mean2(i) = mean2(i)/100;
end
% Means complete
   
sub1 = F1(1:100,:);
sub2 = F2(1:100,:);
var1 = var(sub1);
var2 = var(sub2);
% Variances complete

%%%%% Step 2.1: Testing
prob = [0 0 0 0 0];
predict = zeros(900,5);

for i = 101:1000
    for j = 1:5
        for k = 1:5
            x = F1(i,j);
            num = exp(-0.5*((((x-mean1(k))^2)/var1(k))));
            den = (2*pi*var1(k))^0.5;
            prob(k) = num/den;
        end
        x = max(prob); % Highest prob value
        p = find(prob==x,1,'first'); % Finding index which as prob == x
        predict(i-100,j) = p;
    end
end
% Predictions complete

%%%%% Step 2.2: Calculating accuracy
correct = zeros(900,5);
for i = 1:900
    for j = 1:5
        correct(i,j) = rem(j,6); 
    end
end
count = 0;
for i = 1:900
    for j = 1:5
        if predict(i,j)==correct(i,j)
            count = count+1;
        end
    end
end
accuracy1 = count/4500; % 53% accuracy
error1 = 1-accuracy1;% 47% error
% Accuracy and Error rates complete

%%%%% Step 3: Standard Normal (Z-Score)
Z1 = zeros(1000,5);
for i = 1:1000
    mn = 0;
    ele = F1(i,:);
    % All columns of the specific row
    s = std(ele);
    % single number, sd of all 5 values
    for j = 1:5
        mn = mn+F1(i,j);
    end
    mn = mn/5;
    % mn = mean = Summation/no of elements
    for k = 1:5
        Z1(i,k) = (F1(i,k)-mn)/s;
    end
end
% Z1 complete

c = ['r' 'k' 'g' 'b' 'm'];
for i = 1:5
    hold on
    scatter(Z1(:,i),F2(:,i),[],c(i));
end
xlabel('1st Feature (Z1)')
ylabel('2nd Feature (F2)')
legend('C1', 'C2', 'C3', 'C4', 'C5')
% Plot complete


%%%%% Step 4a: X = Z1
meanZ1 = [0 0 0 0 0];
for i = 1:5
    for j = 1:100
        meanZ1(i) = meanZ1(i) + Z1(j,i);
    end
end
for i = 1:5
    meanZ1(i) = meanZ1(i)/100;
end
% Mean complete
subZ1 = Z1(1:100,:);
varZ1 = var(subZ1);
% Variance complete
probZ1 = [0 0 0 0 0];
predictZ1 = zeros(900,5);
for i = 101:1000
    for j = 1:5
        for k = 1:5
            x = Z1(i,j);
            num = exp(-0.5*((((x-meanZ1(k))^2)/varZ1(k))));
            den = (2*pi*varZ1(k))^0.5;
            probZ1(k) = num/den;
        end
        x = max(probZ1);
        p = find(probZ1==x,1,'first');
        predictZ1(i-100,j) = p;
    end
end
countZ1 = 0;
for i = 1:900
    for j = 1:5
        if predictZ1(i,j)==correct(i,j)
            countZ1 = countZ1+1;
        end
    end
end
accuracyZ1 = countZ1/4500;
errorZ1 = 1-accuracyZ1;


%%%%% Step 4b: X = F2
probF2 = [0 0 0 0 0];
predictF2 = zeros(900,5);
for i = 101:1000
    for j = 1:5
        for k = 1:5
            x = F2(i,j);
            num = exp(-0.5*((((x-mean2(k))^2)/var2(k))));
            den = (2*pi*var2(k))^0.5;
            probF2(k) = num/den;
        end
        x = max(probF2);
        p = find(probF2==x,1,'first');
        predictF2(i-100,j) = p;
    end
end
countF2 = 0;
for i = 1:900
    for j = 1:5
        if predictF2(i,j)==correct(i,j)
            countF2 = countF2+1;
        end
    end
end
accuracyF2 = countF2/4500;
errorF2 = 1-accuracyF2;


%%%%% Step 4c: X = [Z1;F2]
% mean2, meanZ1, var2, varZ1
problast = [0 0 0 0 0];
probF2last = [0 0 0 0 0];
probZ1last = [0 0 0 0 0];
predictlast = zeros(900,5);
for i = 101:1000
    for j = 1:5
        for k = 1:5
            
            x = F2(i,j);
            num1 = exp(-0.5*((((x-mean2(k))^2)/var2(k))));
            den1 = (2*pi*var2(k))^0.5;
            probF2last(k) = num1/den1;
            x = Z1(i,j);
            num2 = exp(-0.5*((((x-meanZ1(k))^2)/varZ1(k))));
            den2 = (2*pi*varZ1(k))^0.5;
            probZ1last(k) = num2/den2;            
            problast(k) = probF2last(k)*probZ1last(k);
        end
        x = max(problast);
        p = find(problast==x,1,'first');
        predictlast(i-100,j) = p;
    end
end
countlast = 0;
for i = 1:900
    for j = 1:5
        if predictlast(i,j)==correct(i,j)
            countlast = countlast+1;
        end
    end
end
accuracylast = countlast/4500;
errorlast = 1-accuracylast;

%%%%% [Z1;Z2]
Z2 = zeros(1000,5);
for i = 1:1000
    mn = 0;
    ele = F2(i,:);
    % All columns of the specific row
    s = std(ele);
    % single number, sd of all 5 values
    for j = 1:5
        mn = mn+F2(i,j);
    end
    mn = mn/5;
    % mn = mean = Summation/no of elements
    for k = 1:5
        Z2(i,k) = (F2(i,k)-mn)/s;
    end
end
meanZ2 = [0 0 0 0 0];
for i = 1:5
    meanZ2(i) = mean(Z2(1:100,i));
end
varZ2 = var(Z2(1:100,:));
problast = [0 0 0 0 0];
probZ2last = [0 0 0 0 0];
probZ1last = [0 0 0 0 0];
predictlast2 = zeros(900,5);
for i = 101:1000
    for j = 1:5
        for k = 1:5            
            x = Z2(i,j);
            num1 = exp(-0.5*((((x-meanZ2(k))^2)/varZ2(k))));
            den1 = (2*pi*varZ2(k))^0.5;
            probZ2last(k) = num1/den1;
            x = Z1(i,j);
            num2 = exp(-0.5*((((x-meanZ1(k))^2)/varZ1(k))));
            den2 = (2*pi*varZ1(k))^0.5;
            probZ1last(k) = num2/den2;            
            problast(k) = probZ1last(k)*probZ2last(k);
        end
        x = max(problast);
        p = find(problast==x,1,'first');
        predictlast2(i-100,j) = p;
    end
end
countlast2 = 0;
for i = 1:900
    for j = 1:5
        if predictlast2(i,j)==correct(i,j)
            countlast2 = countlast2+1;
        end
    end
end
accuracylast2 = countlast2/4500;
errorlast2 = 1-accuracylast2;

%%%%% Comparing accuracy rates
disp(['Accuracy F1:       ', num2str(accuracy1*100),'%']);
disp(['Accuracy Z1:       ', num2str(accuracyZ1*100),'%']);
disp(['Accuracy F2:       ', num2str(accuracyF2*100),'%']);
disp(['Accuracy [Z1 F2]:  ', num2str(accuracylast*100),'%']);
disp(['Accuracy [Z1 Z2]:  ', num2str(accuracylast2*100),'%']);