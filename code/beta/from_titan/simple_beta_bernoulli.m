ab_0 = [3,2; 1,1; 0,1];
delta=0.96;

% Auxiliary Parameters
N       = length(ab_0); % number of skills
dtilde  = ceil(delta/(1-delta));

ss_0 = ab_0;

ss_0(:,1)./(1-delta)