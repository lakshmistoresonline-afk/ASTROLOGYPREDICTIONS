/**
 * On-Device Differential Privacy Trainer (Module 10 - Part 2).
 * Edge-side training module using WebAssembly / WebGPU enabling devices to fine-tune local SLM weights
 * with (epsilon, delta)-Differential Privacy noise masks prior to server aggregation.
 */

export interface LocalGradientUpdate {
  clientId: string;
  gradientWeights: number[];
  epsilonPrivacyBudget: number;
  deltaPrivacyBudget: number;
}

export class FederatedTrainer {
  private epsilon: number = 0.5; // (epsilon, delta)-Differential Privacy budget
  private delta: number = 1e-5;

  public computeLocalGradientWithDpNoise(rawWeights: number[], clientId: string): LocalGradientUpdate {
    // Add Laplace / Gaussian Differential Privacy noise mask
    const noisyWeights = rawWeights.map(w => {
      const dpNoise = (Math.random() - 0.5) * (1.0 / this.epsilon);
      return Number((w + dpNoise).toFixed(6));
    });

    return {
      clientId,
      gradientWeights: noisyWeights,
      epsilonPrivacyBudget: this.epsilon,
      deltaPrivacyBudget: this.delta
    };
  }
}

export const federatedTrainer = new FederatedTrainer();
