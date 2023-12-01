clear 
nums = [0,4,6,8,9,10,11,12,13,14,15,17];
for j = 1:length(nums)
    clear data
    data = load(".\data\Unfiltered\Experimental_data_"+nums(j)+".mat");
    data.wpdata2;
    spdatafilt = zeros(19, 90090);
    wpdatafilt = zeros(19, 90090);
    wpdata2filt = zeros(19, 90090);
    for i = 1:19
        spdatafilt(i, :) = SigFilt(data.spdata(i, :));
        if i<18
            wpdatafilt(i, :) = SigFilt(data.wpdata(i, :));
            wpdata2filt(i, :) = SigFilt(data.wpdata2(i, :));
        end
    end
    data.spdata = spdatafilt;
    data.wpdata = wpdatafilt;
    data.wpdata2 = wpdata2filt;
    data.wpdata2;
    save(".\data\Filtered\2 - Experimental_data_"+nums(j)+".mat","-struct","data")
end
%%
function [Sig_filt] = SigFilt(Sig)

[zF1, pF1, kF1]         = cheby2(4, 20, (30 / (30000 / 2)), 'low');
[bF1, aF1]              = zp2tf(zF1, pF1, kF1);
Sig_filt                = filtfilt(bF1, aF1, Sig);

end