![header](https://capsule-render.vercel.app/api?type=waving&color=4240DD&height=250&section=header&text=KMU%20Baseball%20Report&fontSize=50&fontColor=ffffff&fontAlign=70&fontAlignY=40&desc=Defining%20report%20parameters&descAlign=84&descAlignY=53)

- [투수 리포트 (Pitching Report)](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#투수-리포트-pitching-report)
    - [분석 구간](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#분석-구간)
    - [Pitching Efficiency](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#pitching-efficiency)
    - [Stride Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#stride-phase)
    - [Arm Cocking Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#arm-cocking-phase)
    - [Arm Acceleration Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#arm-acceleration-phase)

<br/>

- [타자 리포트 (Hitting Report)](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#타자-리포트-hitting-report)
    - [분석 구간](https://github.com/parkdragonstone/kookmin-report-explain/blob/master/README.md#분석-구간-1)
    - [Swing Efficiency](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#swing-efficiency)
    - [Loading Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#loading-phase)
    - [Stride Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#stride-phase-1)
    - [Swing Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#swing-phase)

---

## 투수 리포트 (Pitching Report)

### 분석 구간

![pitching_analysis](img/pitching_analysis.png)

- 시점
    1. Knee High (KH) : 무릎을 최대로 들어 올릴 때
    2. Foot Contact (FC) : 스트라이드 다리가 지면과 접촉했을 때
    3. Shoulder Max ER (MER) : 어깨가 최대로 외회전 됐을 때
    4. Ball Release (BR) : 투수가 공을 던지는 시점

- 구간
    1. Stride Phase : KH와 FC 사이의 시간으로 투수가 타자 방향으로 추진하는 단계
    2. Arm Cocking Phase : FC와 MER 사이의 시간으로 투수의 던지는 팔이 외회전 되면서 던지기 전에 에너지를 저장하는 단계
    3. Arm Acceleration : MER과 BR 사이의 시간으로 공을 던지기 위해 팔을 앞으로 회전하고 가속하는 단계
---

### Pitching Efficiency

- ___Kinematic Sequence___
    >- 분절 (골반, 몸통, 팔꿈치, 어깨 or 골반, 몸통, 팔) 회전의 순서와 속도
    >- 몸 전체 속도를 생성하고 전달할 때 효율적인 순서 : 골반 - 몸통 - 팔꿈치 - 어깨 or 골반 - 몸통 - 팔
    >- 몸통은 골반을 기반으로 하여 가속하고 골반은 감속, 팔꿈치는 몸통을 기반으로 하여 가속하고 몸통은 감속하며 회전력이 전달
 
---

### Stride Phase

- ___Hip/Shoulder Separation___
    >- 회전을 통하여 골반 (hip)과 어깨 (shoulder) 사이의 분리된 각도 차이
    >- 하체 (골반)와 상쳬 (어깨) 가 꼬인 정도
    >- Stride Phase 에서는 (-) 값으로 증가할수록 꼬인 정도가 더 크다는 것을 의미


- ___Elbow Flexion___
    >- 팔꿈치가 굽혀지는 각도
    >- (+) 값으로 증가할수록 팔꿈치가 많이 굽혀진 것을 의미

- ___Trail Leg GRF (AP axis)___
    >- 뒷 다리 (축 다리)가 발의 앞 뒤쪽으로 지면을 밀어내는 힘의 크기
    >- (+) 값으로 증가할수록 앞쪽(타자 방향), (-) 값으로 증가할수록 뒤쪽 (2루 방향)으로 지면을 밀어냄

- ___Trail Leg GRF (Vertical)___
    >- 뒷 다리 (축 다리) 가 지면과 수직인 방향으로 지면을 밀어내는 힘의 크기
    >- (+) 값으로 증가할수록 더 큰 힘으로 지면을 밀어냄
### Arm Cocking Phase

- ___Shoulder External Rotation___

- ___Shoulder Horizontal Abduction___
- ___Lead Leg Knee Flexion___
- ___Lead Leg Knee Extention Angular Velocity___
- ___Lead Leg GRF (AP axis)___
- ___Lead Leg GRF (Vertical)___
---

### Arm Acceleration Phase

- Shoulder Abduction
- Trunk Forward Tilt
- Trunk Lateral Tilt
- Lead Leg Knee Flexion
- Lead Leg Knee Extention Angular Velocity
- Lead Leg GRF (AP axis)
- Lead Leg GRF (Vertical)

---
---

## 타자 리포트 (Hitting Report)

### 분석 구간

![hitting_analysis](img/hitting_analysis.png)

- 시점
    1. Toe Off (TO) : 앞 발을 지면에서 떨어졌을 때
    2. Knee High (KH) : 앞 다리의 무릎을 최대로 들어올렸을 때
    3. Foot Contact (FC) : 앞 발이 지면과 접촉하였을 때
    4. Ball Contact (BC) : 공을 임팩트 했을 때

- 구간
    1. Loading Phase : TO와 KH 사이의 시간으로 뒷 발에 체중을 싣는 구간.
    2. Stride Phase : KH와 FC 사이의 시간으로 투수 방향으로 추진하는 구간
    3. Swing Phase : FC와 BC 사이의 시간으로 타자가 스윙하는 구간
---

### Swing Efficiency

- Kinematic Sequence
- X-Factor
- Stride Length
---

### Loading Phase

- Sway [Shank Angle]
- Rear Leg Torque
---

### Stride Phase

- Loss Of Posture [Trunk Lateral Tilt]
- Rear Leg AP GRF
---

### Swing Phase

- Dead Hands [Lead Shoulder - Hand Distance]
- Casting The Hands [Elbow Flexion]
- Loss Of Space 1 [Pelvis Open Timing]
- Loss Of Space 2 [Lead Shoulder - Hand  Distance]
- Loss Of Space 3 [Elbow Height]
- Rear Leg Ground Reaction Force [Vertical]
- Rear Leg Torque
- Lead Leg Ground Reaction Force (Vertical)
- Lead Leg Torque
- Rear & Lead Leg Ground Reaction Force (AP axis)
- Rear Shoulder Ad/Abduction Angular Velocity
- Lead Leg Knee Extension Angular Velocity
- Lead Elbow Extension Angular Velocity
- Trunk Lateral Tilt