#-------------------------
#Binary endpoint, number of patietns per arm
#-------------------------
n_binary <- function(alpha, beta, pi1, pi2)
pi <- (pi1+pi2)/2. #change back to original
za <- qnorm(1-alpha/2.)*sqrt(2*pi*(1-pi))+ qnorm(1-beta)*sqrt(pi1*(1-pi1)+pi2*(1-pi2))
  #number of patients per arm
  nevents <- za^2/((pi2-pi1)^2)
  return(nevents)
}

n_binary(0.05, 0.1, 0.56, 0.66)

#Method 2
n_binary2 <- function(alpha, beta, pi1, pi2)
{ pi <- (pi1+pi2)/2.
za <- (qnorm(1-alpha/2.)+ qnorm(1-beta))^2*(pi1*(1-pi1)+pi2*(1-pi2))
#number of patients per arm
nevents <- za/((pi2-pi1)^2)
return(nevents)
}

n_binary2(0.05, 0.1, 0.56, 0.66)

#Sample Size for binary data, assuming equal numbers are to be randomized to each group
#number of patients in each group
#same as n_binary2()
n_sample <- function(alpha, beta, p1, p2)
{
  za<-qnorm(1-alpha/2.)+ qnorm(beta)
  n <- za^2*(p1*(1-p1)+p2*(1-p2))/(p1-p2)^2
  return(n)
}

n_sample(alpha=0.05, beta=0.8, p1=0.7, p2=0.9)

n_sample(alpha=0.05, beta=0.8, p1=0.5, p2=0.85)

#With continuity corrections
n_binary_correction <- function(alpha, beta, pi1, pi2)
{
delta <- pi2-pi1
pi <- (pi1+pi2)/2.
za <- qnorm(1-alpha/2.)*sqrt(2*pi*(1-pi))+ qnorm(1-beta)*sqrt(pi1*(1-pi1)+pi2*(1-pi2))
#number of patients per arm
nevents <- za^2/(delta^2)
nevents  <- nevents/4.*(1+sqrt(1+4./(nevents*delta)))^2
return(nevents)
}

n_binary_correction(0.05, 0.1, 0.56, 0.66)

#Method 3, use Odds Ratio
#or: odds ratio
n_binary3 <- function(alpha, beta, pi1, or)
{ pi2 <- or*pi1/(1-pi1+or*pi1)
  pi <- (pi1+pi2)/2.
za <- qnorm(1-alpha/2.)*sqrt(2*pi*(1-pi))+ qnorm(1-beta)*sqrt(pi1*(1-pi1)+pi2*(1-pi2))
#number of patients per arm
nevents <- za^2/((pi2-pi1)^2)
return(nevents)
}

n_binary3(0.05, 0.1, 0.56, 2.)

#use method 2 (approximation method)
#or: odds ratio
n_binary32 <- function(alpha, beta, pi1, or)
{
pi2 <- or*pi1/(1-pi1+or*pi1)
pi <- (pi1+pi2)/2.
za <- (qnorm(1-alpha/2.)+ qnorm(1-beta))^2*(pi1*(1-pi1)+pi2*(1-pi2))
#number of patients per arm
nevents <- za/((pi2-pi1)^2)
return(nevents)
}
n_binary32(0.05, 0.1, 0.56, 2.)

#Q2.5
n_binary2(0.05, 0.1, 0.25, 0.65)
n_binary(0.05, 0.1, 0.25, 0.65)


#-------------------------------------
#Total Number of events for time to event data
#-------------------------------------
#Assuming Exponential Survival
n_event <- function(alpha, beta, pa, pb, hz)
{
za<-qnorm(1-alpha/2.)+ qnorm(beta)
#total number of events for two groups
nevents <- za^2/(pa*pb*(log(hz))^2)
return(nevents)
}

#Q7.1
hz <- 1.5
n_event(alpha=0.05, beta=0.9, pa=0.5, pb=0.5, hz)
n_event(alpha=0.05, beta=0.9, pa=0.5, pb=0.5, 0.6)

#Proportional Hazards Only
#total number of events
n_event_ph <- function(alpha, beta, hz)
{
  za<-qnorm(1-alpha/2.)+ qnorm(beta)
  #total number of events for two groups
  nevents <- za^2*(hz+1)^2/((hz-1)^2)
  return(nevents)
}

#Q7.2
hz <- 1.5
n_event_ph(alpha=0.05, beta=0.9, hz)

