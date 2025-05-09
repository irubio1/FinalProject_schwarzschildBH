program SchwarzschildGeodesics
    implicit none
    real(8) :: r, phi, tau, t, dr, dphi, dt
    real(8) :: E, L, M_BH, dtau, tau_end
    real(8) :: k1r, k2r, k3r, k4r
    real(8) :: k1phi, k2phi, k3phi, k4phi
    real(8) :: k1t, k2t, k3t, k4t
    real(8) :: f_r, f_phi
	integer(8) :: i, n_steps
    real(8), parameter :: pi = 4.0d0 * atan(1.0d0)

	! Open file and read simulation parameters from initial_values.txt
	open(unit=1, file='initial_values.txt')
	read(1,*) n_steps, r, tau_end, L, E, M_BH, phi, dtau
	close(1)
  
    tau = 0.0d0        ! initial proper time

   
    ! Output file
    open(unit=10, file="trajectory.dat", status="replace")
    write(10,'(A)') "# tau      r(tau)      phi(tau)      t(tau)"
    write(10,'(F10.6,1X,F10.6,1X,F10.6)') tau, r, phi

    ! RK4 Integration loop
    do i = 1, n_steps
	    ! --- RK4 for r ---
	    k1r = dtau * dr_dtau(r, E, L, M_BH)
	    k2r = dtau * dr_dtau(r + 0.5d0*k1r, E, L, M_BH)
	    k3r = dtau * dr_dtau(r + 0.5d0*k2r, E, L, M_BH)
	    k4r = dtau * dr_dtau(r + k3r, E, L, M_BH)
	    r = r + (k1r + 2.0d0*k2r + 2.0d0*k3r + k4r) / 6.0d0

	    ! --- RK4 for phi ---
	    k1phi = dtau * dphi_dtau(r, L)
	    k2phi = dtau * dphi_dtau(r + 0.5d0*k1r, L)
	    k3phi = dtau * dphi_dtau(r + 0.5d0*k2r, L)
	    k4phi = dtau * dphi_dtau(r + k3r, L)
	    phi = phi + (k1phi + 2.0d0*k2phi + 2.0d0*k3phi + k4phi) / 6.0d0

	    ! --- RK4 for t ---
	    k1t = dtau * dt_dtau(E, M_BH, r)
	    k2t = dtau * dt_dtau(E, M_BH, r + 0.5d0*k1r)
	    k3t = dtau * dt_dtau(E, M_BH, r + 0.5d0*k2r)
	    k4t = dtau * dt_dtau(E, M_BH, r + k3r)
	    t = t + (k1t + 2.0d0*k2t + 2.0d0*k3t + k4t) / 6.0d0

	    tau = tau + dtau
	    write(10,'(F10.6,1X,ES14.6,1X,ES14.6,1X,ES14.6)') tau, r, phi, t
	end do


    close(10)
    print *, "Trajectory saved to trajectory.dat"

contains

    function dr_dtau(r, E, L, M_BH) result(dr)
        implicit none
        real(8), intent(in) :: r, E, L, M_BH
        real(8) :: dr, Veff
        ! Effective potential
        Veff = (1.0d0 - 2.0d0*M_BH / r) * (1.0d0 + (L**2) / (r**2))
        if (E**2 >= Veff) then
            print *, "Warning: r at or below Schwarzschild radius: r =", r
            dr = sqrt(E**2 - Veff)
        else
            dr = 0.0d0
        endif
    end function dr_dtau

    function dphi_dtau(r, L) result(dphi)
        implicit none
        real(8), intent(in) :: r, L
        real(8) :: dphi
        if (r <= 0.0d0) then
            print *, "Warning: r <= 0 in dphi_dtau"
            dphi = 0.0d0
        else
            dphi = L / (r**2)
        endif
    end function dphi_dtau

    function dt_dtau(E, M_BH, r) result(dt)
    	implicit none
    	real(8), intent(in) :: E, M_BH, r
    	real(8) :: dt
    	if (r <= 2.0d0 * M_BH) then
            print *, "Warning: r at or below Schwarzschild radius: r =", r
            dt = 0.0d0
        else
            dt = E / (1.0d0 - 2.0d0 * M_BH / r)
        endif

    end function dt_dtau

end program SchwarzschildGeodesics