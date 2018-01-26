% Basic example on the creation of a set of ROC curves for the Energy detector
% based on analytical expressions and MonteCarlo simulation
% Furher reading: 
%   - A Survey of Spectrum Sensing Algorithms for Cognitive Radio Applications, Yucek and Arslan, 
%   - Energy Detection for Spectrum Sensing in Cognitive Radio, S. Atapattu et al
%
% Germán Augusto Ramírez Arroyave
% Universidad Nacional de Colombia 
% CMUN August, 2017

close all; clear; clc;
%% Used Variables
N=32;                           % number of time samples
R=1;                            % reference resistance
W=-80;                          % noise power level in dBm
S=[-85:2:-81,-80,-79:2:-75];    % set of signal power levels in dBm
minEnTh=-70;                    % minimum energy threshold in mJ
maxEnTh=-50;                    % maximum energy threshold in mJ
K=21;                           % number of samples for the target Pf in the MonteCarlo simulation
L=10000;                        % number of MonteCarlo simulations (this could take a while...)
h=ones(1,N);                    % dummy transfer function (later iterations should consider channel model)

sigma_w_2=10.^((W-30)/10);      % (circularly symmetric) noise variance in W (2\sigma_w^2 in literature)
sigma_s_2=10.^((S-30)/10);      % (noise) signal variance in W
s_amp=sqrt(0.5*R*sigma_s_2);    % (real and imaginary parts) signal amplitude in volts 
n_amp=sqrt(0.5*R*sigma_w_2);    % noise amplitude in volts 
lambda=10.^(linspace(minEnTh-30,maxEnTh-30,101)/10); % energy threshold in dBJ for detection (used for analytical curves only)


%% Creation of a set of plots based on the analytical expressions
x=lambda./sigma_w_2;
xx=zeros(length(S),length(lambda));
for cont=1:length(S)
    xx(cont,:)=lambda./(sigma_w_2+sigma_s_2(cont));
end

Pf=gammainc(x,N,'upper');   %this is due to the way in which Matlab calculates the incomplete gamma function.
Pfa=qfunc((lambda-N*sigma_w_2)/(sqrt(N)*sigma_w_2));    %alternative (approximate) expression for Pf by means of central limit theorem
Pd=gammainc(xx,N,'upper');  %Pd=1-gammainc(xx,N,'lower');	%use in case of numerical stability issues

semilogx(lambda,Pd,'linewidth',2);
set(gcf, 'Units','inches', 'Position',[0 0 10 6.2], 'PaperPositionMode','auto') 
set(gca, 'FontSize', 12, 'LineWidth', 1);
grid on; title(['Detection probability in terms of threshold for \sigma_w^2=', num2str(W), 'dBm, and N=', num2str(N)]);
xlabel('\lambda: Detection threshold value'); ylabel('Pd: detection probability');
legendStr=cellstr(num2str((S-W)', 'SNR= %-d dB')); legend(legendStr,'Location','SouthWest');

figure, semilogx(lambda,Pf,lambda,Pfa,'r','linewidth',2);
set(gcf, 'Units','inches', 'Position',[0 0 10 6.2], 'PaperPositionMode','auto') 
set(gca, 'FontSize', 12, 'LineWidth', 1);
grid on; title(['False alarm probability in terms of threshold for \sigma_w^2=', num2str(W), 'dBm, and N=', num2str(N)]); 
xlabel('\lambda: Detection threshold value'); ylabel('Pf: false alarm probability');
legend('Accurate','CLT approximation');

figure, semilogx(Pf,Pd,'-*','linewidth',2);
set(gcf, 'Units','inches', 'Position',[0 0 10 6.2], 'PaperPositionMode','auto') 
set(gca, 'FontSize', 12, 'LineWidth', 1);
grid on; title('Analytical ROC curve for Energy detector'); axis([1e-10 1 0 1]);
xlabel('Pf: false alarm probability'); ylabel('Pd: detection probability');
legendStr=cellstr(num2str((S-W)', 'SNR= %-d dB')); legend(legendStr,'Location','SouthEast');


%% Monte Carlo simulation, approach 1: make some signal realizations varying the target PF and create an empirical ROC curve
ind=1;                      %initialize variables to be used within the loop
simPd=zeros(K,length(S));   %simulated probabilities are arranged row-wise because of the format accepted by the plot function
simPf=zeros(K,length(S));
E_y=zeros(length(S),1);
P_y=zeros(length(S),1);
thr=zeros(1,K);

for targPf=logspace(-7,0,K)
    thr(ind)=sigma_w_2*gammaincinv(targPf,N,'upper');           %Detection threshold according to the analytical expression for Pf
%   thr(ind)=sigma_w_2*sqrt(N)*(qfuncinv(simPf)+sqrt(N)); 	%Detection threshold according to the approximate expression for Pf (enable to see the differences)
    contPd=zeros(length(S),1);
    contPf=zeros(length(S),1);
	contTrue=0;

    for cont=1:L %Do a series of Monte-Carlo runs
        n=n_amp*randn(length(S),N) + 1i*n_amp*randn(length(S),N); 
        theta=randi(2)-1;                                           %(on average) half samples will be '1' and half will be '0'
        s=theta*s_amp.'*randn(1,N)+theta*1i*s_amp.'*randn(1,N);     %external product to create a set of 'noisy signals'
        y = s + n;                                                  
%       y=ifft(bsxfun(@times,fft(h),fft(s,[],2)),[],2)+n;      %fast convolution to include channel model... not tested yet
        E_y=sum(abs(y).^2,2);                               %energy for each realization
        if theta
            contTrue=contTrue+1;
            contPd=contPd+(E_y>thr(ind));                   %count the number of true detections
            P_y=P_y+E_y/N;
        else
            contPf=contPf+(E_y>thr(ind));                   %count the number of false detections
        end
        
    end       
% %     simPd(ind,:)=2*contPd/L;        %get empirical probability (statistically L/2 true and false examples)
% %     simPf(ind,:)=2*contPf/L;        %NOTE: it seems that L=10000 is not large enough for this assumption to hold
    simPd(ind,:)=contPd/contTrue;       %get empirical probability taking int account the actual number of true examples
	simPf(ind,:)=contPf/(L-contTrue);	  
    ind=ind+1;    
end
P_y=10*log10(P_y/(K*L/2));

targPf=logspace(-7,0,K);
figure;semilogx(targPf,simPd,'o', Pf,Pd, 'linewidth',2); %generate the ROC curve
set(gcf, 'Units','inches', 'Position',[0 0 10 6.2], 'PaperPositionMode','auto') 
set(gca, 'FontSize', 12, 'LineWidth', 1);
grid on; title('Simulated and Analytical ROC curve for Energy detector'); axis([1e-7 1 0 1]);
xlabel('Pf: false alarm probability'); ylabel('Pd: detection probability');
legendStr=cellstr(num2str((S-W)', 'SNR= %-d dB S')); legendStr=[legendStr; cellstr(num2str((S-W)', 'SNR= %-d dB T'))];
legend(legendStr,'Location','SouthEast');

figure;plot(targPf,simPd,'o', simPf,simPd,'+', Pf,Pd, 'linewidth',2); %generate the ROC curve in linear scale
set(gcf, 'Units','inches', 'Position',[0 0 10 6.2], 'PaperPositionMode','auto') 
set(gca, 'FontSize', 12, 'LineWidth', 1);
grid on; title('Simulated and Analytical ROC curve for Energy detector'); axis([1e-7 1 0 1]);
xlabel('Pf: false alarm probability'); ylabel('Pd: detection probability');
legendStr=cellstr(num2str((S-W)', 'SNR= %-d dB S')); legendStr=[legendStr; cellstr(num2str((S-W)', 'SNR= %-d dB R'))]; legendStr=[legendStr; cellstr(num2str((S-W)', 'SNR= %-d dB A'))];
legend(legendStr,'Location','SouthEast');


%% Monte Carlo simulation, approach 2: make some signal realizations varying threshold and create empirical ROC curve
% ind=1;
% simPd=zeros(K,length(S)); %simulated probabilities are arranged row-wise because of the format accepted by the plot function
% simPf=zeros(K,length(S));
% En=zeros(length(S),1);
% 
% for thr=10.^(linspace(-10,-8,101)) % power threshold for detection (linear scale)
%     contPd=zeros(length(S),1);
%     contPf=zeros(length(S),1);
%     contTrue=0;
%     for cont=1:L
%         n=n_amp*randn(length(S),N)+1i*n_amp*randn(length(S),N); 
%         theta=randi(2)-1;
%         s=theta*s_amp.'*randn(1,N)+theta*1i*s_amp.'*randn(1,N);
%         y=s+n;
% %        y=ifft(bsxfun(@times,fft(h),fft(s,[],2)),[],2)+n; 
%         En=sum(abs(y).^2,2);
%         if theta
%             contTrue=contTrue+1;
%             contPd=contPd+(En>thr);
%         else
%             contPf=contPf+(En>thr);
%         end
%     end
%     simPd(ind,:)=contPd/contTrue;   
%     simPf(ind,:)=contPf/(L-contTrue);	
%     ind=ind+1;    
% end
% 
% figure;semilogx(simPf,simPd,'o', Pf,Pd, 'linewidth',2); %generate the ROC curve
% grid on; title('Simulated and Analytical ROC curve for Energy detector'); axis([1e-6 1 0.5 1]);
% xlabel('Pf: false alarm probability'); ylabel('Pd: detection probability');
% legendStr=cellstr(num2str((S-W)', 'SNR= %-d dB S')); legendStr=[legendStr; cellstr(num2str((S-W)', 'SNR= %-d dB A'))]; 
% legend(legendStr,'Location','SouthEast');