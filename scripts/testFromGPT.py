import numpy as np
import matplotlib.pyplot as plt

def far_field_square_aperture():
    # 1) Grid and sampling
    Nx, Ny = 256, 256              # Number of points
    dx, dy = 10e-6, 10e-6          # Grid spacing (10 µm, for example)
    x = (np.arange(-Nx//2, Nx//2)) * dx
    y = (np.arange(-Ny//2, Ny//2)) * dy
    xx, yy = np.meshgrid(x, y)

    # 2) Define the square aperture:
    #    Let the square side be 1.0 mm
    aperture_side = 0.05e-3         # 1 mm
    half_side = aperture_side  # half side

    # Create the field array
    U0 = np.zeros((Ny, Nx), dtype=np.complex128)

    # Boolean mask: True inside the square, False outside
    inside_square = (np.abs(xx) <= half_side) & (np.abs(yy) <= half_side)
    U0[inside_square] = 1.0  # uniform amplitude = 1.0 within the square

        # 4) Plot
    plt.figure(figsize=(6,5))
    plt.imshow(U0.real, origin='lower',# cmap='viridis',
               extent=[-0.5, 0.5, -0.5, 0.5])
    plt.colorbar(label="Intensity [a.u.]")
    plt.title("Real of U0 (Square Aperture)")
    plt.xlabel("Spatial freq (arb. units)")
    plt.ylabel("Spatial freq (arb. units)")
    plt.tight_layout()
    plt.show()

    # 4) Plot
    plt.figure(figsize=(6,5))
    plt.imshow(U0.imag, origin='lower')#, cmap='viridis'),
#               extent=[-0.5, 0.5, -0.5, 0.5])
    plt.colorbar(label="Intensity [a.u.]")
    plt.title("Imag of U0 (Square Aperture)")
    plt.xlabel("Spatial freq (arb. units)")
    plt.ylabel("Spatial freq (arb. units)")
    plt.tight_layout()
    plt.show()
    
    print(U0)

#    
#    phase_factor = np.pi
#    # (Optional) Add phase if desired:
#    U0 *= np.exp(1j * phase_factor * xx)

    # 3) Compute the far-field via 2D FFT
    #    We use ifftshift -> fft2 -> fftshift
    U0_fft = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(U0)))
    far_field_intensity = np.abs(U0_fft)**2
    p = np.angle(U0_fft)
    print(U0_fft.real)
    print(U0_fft.imag)

    # 4) Plot
    plt.figure(figsize=(6,5))
    plt.imshow(far_field_intensity, origin='lower',# cmap='viridis',
               extent=[-0.5, 0.5, -0.5, 0.5])
    plt.colorbar(label="Intensity [a.u.]")
    plt.title("Far-Field Diffraction (Square Aperture)")
    plt.xlabel("Spatial freq (arb. units)")
    plt.ylabel("Spatial freq (arb. units)")
    plt.tight_layout()
    plt.show()

    # 4) Plot
    plt.figure(figsize=(6,5))
    plt.imshow(p, origin='lower')#, cmap='viridis'),
#               extent=[-0.5, 0.5, -0.5, 0.5])
    plt.colorbar(label="Intensity [a.u.]")
    plt.title("Far-Field Phase (Square Aperture)")
    plt.xlabel("Spatial freq (arb. units)")
    plt.ylabel("Spatial freq (arb. units)")
    plt.tight_layout()
    plt.show()
    
    # 4) Plot
    plt.figure(figsize=(6,5))
    plt.imshow(U0_fft.real, origin='lower')#, cmap='viridis'),
#               extent=[-0.5, 0.5, -0.5, 0.5])
    plt.colorbar(label="Intensity [a.u.]")
    plt.title("Far-Field Real Part (Square Aperture)")
    plt.xlabel("Spatial freq (arb. units)")
    plt.ylabel("Spatial freq (arb. units)")
    plt.tight_layout()
    plt.show()
    
    # 4) Plot
    plt.figure(figsize=(6,5))
    plt.imshow(U0_fft.imag, origin='lower')#, cmap='viridis'),
#               extent=[-0.5, 0.5, -0.5, 0.5])
    plt.colorbar(label="Intensity [a.u.]")
    plt.title("Far-Field Imag Part (Square Aperture)")
    plt.xlabel("Spatial freq (arb. units)")
    plt.ylabel("Spatial freq (arb. units)")
    plt.tight_layout()
    plt.show()
    
    print(np.min(p))
    print(np.max(p))

if __name__ == "__main__":
    far_field_square_aperture()
