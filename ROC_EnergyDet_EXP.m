% Experimental gnuradio, ROC curves for the energy detector
%
% Germán Augusto Ramírez Arroyave
% Universidad Nacional de Colombia 
% CMUN 2017

clear, clc;
% %% Read data
SNR={'-5'};%,'-3','-1','0','1','3','5'};
for cont=1:length(SNR)
%     N_det_path=['C:\Users\usuario\Documents\gnuRadio\Misc\SpectrumSensing\Simulation\SNR=', num2str(SNR{cont}), '\N_det.dat'];
%     N_inD_path=['C:\Users\usuario\Documents\gnuRadio\Misc\SpectrumSensing\Simulation\SNR=', num2str(SNR{cont}), '\N_inD.dat'];
%     thr_path=['C:\Users\usuario\Documents\gnuRadio\Misc\SpectrumSensing\Simulation\SNR=', num2str(SNR{cont}), '\Thr.dat'];
    
    N_det_path=['C:\Users\usuario\Documents\gnuRadio\Misc\SpectrumSensing\USRP_exp\SNR=', num2str(SNR{cont}), '\N_det_exp.dat'];
    N_inD_path=['C:\Users\usuario\Documents\gnuRadio\Misc\SpectrumSensing\USRP_exp\SNR=', num2str(SNR{cont}), '\N_inD_exp.dat'];
    thr_path=['C:\Users\usuario\Documents\gnuRadio\Misc\SpectrumSensing\USRP_exp\SNR=', num2str(SNR{cont}), '\Thr_exp.dat'];

	N_det{cont}=read_fromGNUradio(N_det_path,'float');
    N_inD{cont}=read_fromGNUradio(N_inD_path,'float');
    thr{cont}=read_fromGNUradio(thr_path,'float');   
end

%% analytical expression for Pd
targPf = logspace(-6,0,21);
S = -80;%[-160,-120,-81,-80,-79,-77,-75];
W = -80.0;
Ndat=32;
sigma_s_2 = 10.^(S/10);
sigma_w_2 = 10^(W/10);
lambda = sigma_w_2*gammaincinv(targPf,Ndat,'upper');
for cont=1:length(S)
    xx(cont,:)=lambda./(sigma_w_2+sigma_s_2(cont));
end
Pd=gammainc(xx,Ndat,'upper');

%% Plot ROC curves and other interesting figures
for cont_snr=1:length(SNR)
    [N,bins]=histc(thr{cont_snr},unique(thr{cont_snr}));
    base=0;
    for cont_thr=1:length(N)
        expPd(cont_snr,cont_thr)=sum(N_det{cont_snr}(base+1:base+N(cont_thr)))/sum(N_inD{cont_snr}(base+1:base+N(cont_thr)));
        base=base+N(cont_thr);
        threshold(cont_snr,:)=unique(thr{cont_snr});
    end
end
threshold=unique(threshold);

%% Figures
figure, semilogx(targPf,Pd,'linewidth',2);hold on, semilogx(targPf,expPd,'*','linewidth',2); %plot(expPd,'-*')
grid on; title('Detection probability in terms of threshold'); 
xlabel('False alarm probability (expected)'); ylabel('Pd: detection probability');
legendStr=cellstr(num2str((S-W)', 'SNR= %-d dB T')); legendStr=[legendStr; cellstr(num2str((S-W)', 'SNR= %-d dB S'))];
legend(legendStr,'Location','SouthEast');

figure, plot(lambda,'b-+','linewidth',2), hold on, plot(threshold(end:-1:1),'r-*','linewidth',2);
grid on; title('Detection threshold'); legend('analytical','experimental');
ylabel('Iteration number'); ylabel('\lambda: Detection threshold value'); 