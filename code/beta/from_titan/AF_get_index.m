% The function get_index takes in parameters and states and returns the
% indices for the optimal policy in Alon-Fershtman 2019.

function Ij_0 = AF_get_index(delta,ab_0,ss_0)

% Auxiliary Parameters
N       = length(ab_0); % number of skills
dtilde  = ceil(delta/(1-delta));

% Calculate Initial Index for Each Skill:
I_00 = dtilde.*( (delta.^(dtilde-sum(ss_0,2))) ./ sum(ss_0,2) );
I_0  = (ss_0(:,1)./(1-delta)).*I_00;

gradregion_j = (sum(ss_0,2)>=dtilde); % check if any skill in graduation region

Ij_0 = nan(N,1);  % initial indices
Ij_0(gradregion_j==0) = I_0(gradregion_j==0,1); 
Ij_0(gradregion_j==1) = ss_0(gradregion_j==1,1)./(1-delta); % = human capital / 1-delta if in graduation region


end