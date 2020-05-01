
% AF_model_predict takes the parameter inputs, solves the model, and
% calculates predictions of the moments we are trying to fit.

function [field_i,state_i,ptrue_i,sst_mat,ss0_mat,study_history]=AF_model_predict(ab_0,delta,sys_param)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Parse System Parameters
sim_num   = cell2mat(sys_param(1));
Tscale    = cell2mat(sys_param(2));
yrs_GenEd = cell2mat(sys_param(3));
N         = cell2mat(sys_param(4));
yrs_InitEd= cell2mat(sys_param(6));

% Auxilary Parameters
dtilde  = ceil(delta/(1-delta));
t_GenEd = ceil(Tscale*(yrs_GenEd+yrs_InitEd)/N); % time split equally across skills, round up to keep integer values.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Initialize Results to Be Stored
field_i   = nan(sim_num,1); % sim_num x 1 - field (number) specialized in
state_i   = nan(sim_num,2); % sim_num x 2 - a_t,b_t
ptrue_i   = nan(sim_num,N); % sim_num x N matrix, element x_ij is person i's true ability in skill j. Note ptrue_i(i,field_i(i)) = ability in chosen specialization.
ss0_mat   = nan(N,2,sim_num); % Nx2 matrix for each sim_num (3rd-dimension) with state (a_hs,b_hs) of each skill when finished manadatory general education
sst_mat   = nan(N,2,sim_num); % as above, but at the end of education (hs + post secondary).


% Solve Model %

parfor i = 1:sim_num % for each person
    
% Each Individual Draws Ability from Nature
p_true  = betarnd(ab_0(:,1),ab_0(:,2)); % Nx1 vector of true skill, p_j, drawn from population distribution

 
%%% General Education Period %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 



% Studying: High School General Education
study_hs = binornd(t_GenEd,p_true);

% Update State:
ss_0 = ab_0 + [study_hs,t_GenEd-study_hs]; 


%%% Post-Secondary Education %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Initialize
ss_t          = ss_0; % initialize current state -  {At=at+a0,Bt=bt+b0}
Ij_t          = AF_get_index(delta,ab_0,ss_t); % initialize skill indices

% auxiliary variables
this_history =nan;
keep_studying = 1;
while keep_studying==1
    
    
    % Pick field to invest in
    max_fields = find(Ij_t==max(Ij_t));
    this_field = datasample(max_fields,1);
    
    % Graduate or Continue to Study?
    
    % Graduate if.,,
    if sum(ss_t(this_field,:))>=dtilde % Chosen skill in graduation region
        field_chosen  = this_field;
        field_state   = ss_t(this_field,:); % {At=at+a0,Bt=bt+b0}
        break
    end

    
    % Continue to study...
        
    % record study history if studying
    this_history = [this_history,this_field]; % field studied
    
    % attempt to study
    study_j            = binornd(1,p_true(this_field)); % try to learn
    ss_t(this_field,:) = ss_t(this_field,:) + [study_j,1-study_j]; % update state    
    
   
    % Update Index
    Ij_t = AF_get_index(delta,ab_0,ss_t); % using new state
        
    
    % Now return to beginning and choose next field to invest in...
    
    
end

% record results
field_i(i,1)     = field_chosen; % sim_num x 1 - field (number) specialized in
state_i(i,:)     = field_state; % sim_num x 2 - a_t,b_t
ptrue_i(i,:)     = p_true'; % sim_num x N matrix, element x_ij is person i's true ability in skill j. Note ptrue_i(i,field_i(i)) = ability in chosen specialization.
sst_mat(:,:,i)   = ss_t; % as above, but at the end of education (hs + post secondary).
ss0_mat(:,:,i)   = ss_0;
study_history(i,1) = {this_history(2:end)}; % field studied

 
% simulate next individual
%clear field_chosen ss_0 ss_t p_true study_hs Ij_t field_state this_history


end




end

