![header](https://capsule-render.vercel.app/api?type=waving&color=4240DD&height=250&section=header&text=KMU%20Baseball%20Report&fontSize=50&fontColor=ffffff&fontAlign=70&fontAlignY=40&desc=Defining%20report%20parameters&descAlign=84&descAlignY=53)

- [투수 리포트 (Pitching Report)](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#투수-리포트-pitching-report)
  <br><br>
    1. [분석 구간](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#분석-구간)
    2. [Pitching Efficiency](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#pitching-efficiency)
    3. [Stride Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#stride-phase)
    4. [Arm Cocking Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#arm-cocking-phase)
    5. [Arm Acceleration Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#arm-acceleration-phase)

<br/>

- [타자 리포트 (Hitting Report)](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#타자-리포트-hitting-report)
<br><br>
    1. [분석 구간](https://github.com/parkdragonstone/kookmin-report-explain/blob/master/README.md#분석-구간-1)
    2. [Swing Efficiency](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#swing-efficiency)
    3. [Loading Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#loading-phase)
    4. [Stride Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#stride-phase-1)
    5. [Swing Phase](https://github.com/parkdragonstone/kookmin-report-explain?tab=readme-ov-file#swing-phase)

---

## 투수 리포트 (Pitching Report)

### 분석 구간

<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/pitching_analysis.png" width = 600>


- 시점
    1. Knee High `KH` : 무릎을 최대로 들어 올릴 때
    2. Foot Contact `FC` : 스트라이드 다리가 지면과 접촉했을 때
    3. Shoulder Max ER `MER` : 어깨가 최대로 외회전 됐을 때
    4. Ball Release `BR` : 투수가 공을 던지는 시점

- 구간
    1. Stride Phase : `KH` 와 `FC` 사이의 시간으로 투수가 타자 방향으로 추진하는 단계
    2. Arm Cocking Phase : `FC` 와 `MER` 사이의 시간으로 투수의 던지는 팔이 외회전 되면서 던지기 전에 에너지를 저장하는 단계
    3. Arm Acceleration Phase : `MER` 과 `BR` 사이의 시간으로 공을 던지기 위해 팔을 앞으로 회전하고 가속하는 단계
---

### Pitching Efficiency

- ___Kinematic Sequence___
1. 골반 - 몸통 - 팔 - 어깨
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/ks_4.png" width = 600>

2.  골반 - 몸통 - 팔
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/ks_3.png" width = 600>

> - 분절 (`골반, 몸통, 팔꿈치, 어깨` or `골반, 몸통, 팔`) 회전의 순서와 속도
> - 몸 전체 속도를 생성하고 전달할 때 ___효율적인 순서___ : `골반 -> 몸통 -> 팔꿈치 -> 어깨` or `골반 -> 몸통 -> 팔`
> - 몸통은 골반을 기반으로 하여 가속하고 골반은 감속, 팔꿈치는 몸통을 기반으로 하여 가속하고 몸통은 감속하며 회전력이 전달 : 2번의 사진 처럼 빨간색 (골반) 그래프의 피크점을 타고 초록색 (몸통) 이 증가하고, 초록색 그래프이 피크점을 타고 파란색 (팔)의 그래프가 증가하는 것이 이상적임
> - `Speed Gain` : `다음 분절 각속도 / 이전 분절 각속도`를 통해 얻어지는 것이며, 1.4 이상이 효율적으로 각속도가 다음 분절로 전달 되었다는 것을 의미
---
### Stride Phase
- ___Height of Knee & Pelvis___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/KneePelHeight.png" width = 600>

> - 투수가 진행 방향으로 전진할 때, 무릎과 골반의 높이를 관잘

- ___Hip/Shoulder Separation___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/xfactor.png" width = 600>

> - 회전을 통하여 골반 (hip)과 어깨 (shoulder) 사이의 분리된 각도 차이
> - 하체 (골반)와 상쳬 (어깨) 가 꼬인 정도
> - `Stride Phase`에서는 `-` 값으로 증가할수록 꼬인 정도가 더 크다는 것을 의미
> - 과도한 꼬임은 선수가 회전하는 능력이 부족하면 오히려 투구 동작에 좋지 않은 영향을 미칠수 있음
> - `FC` 이후에 최대 꼬임이 나타나는 것이 적절한 타이밍이라 할수 있음

- ___Elbow Flexion___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/elbowflex.png" width = 600>

> - 팔꿈치가 굽혀지는 각도
> - `180°`로 갈수록 팔꿈치가 굽혀지는, `0°`으로 갈수록 팔꿈치가 펴지는 것을 의미
> - 회전할 때 팔꿈치가 빠른 시점에 펴지기 시작하면 회전하는데 더 많은 힘과 팔꿈치에 부하가 더 커지기 때문에 적절한 타이밍에 팔을 펴는것이 중요함
> - `FC` 이후에 최대점이 나타나고 `MER`까지 최대한 유지하고 `Arm Acceleration Phase`에서 급격하게 0° 방향으로 그래프가 움직이는 것이 적절할 것으로 판단됨

- ___Trail Leg GRF (AP axis)___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/trailgrfAP.png" width = 600>

> - 뒷 다리 (축 다리)가 발의 앞 뒤쪽으로 지면을 밀어내는 힘의 크기
> - `+` 값으로 증가할수록 앞쪽(타자 방향), `-` 값으로 증가할수록 뒤쪽 (2루 방향)으로 지면을 밀어냄

- ___Trail Leg GRF (Vertical)___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/trailgrfV.png" width = 600>

> - 뒷 다리 (축 다리) 가 지면과 수직인 방향으로 지면을 밀어내는 힘의 크기
> - `+` 값으로 증가할수록 더 큰 힘으로 지면을 밀어냄
---

### Arm Cocking Phase

- ___Shank Lateral Tilt___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/ShankTilt.png" width = 600>

> - `FC`에서 앞 다리의 정강이가 측면으로 얼마나 기울었는지를 관찰
> - 정강이가 바닥과 수직일 때 각도를 0°라고 했을 때, 정강이가 안쪽으로 기울어지면 `-`값으로 증가하고 바깥으로 기울어지면 `+`값으로 증가한다.

- ___Shoulder External Rotation___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/SER.png" width = 600>

> - 어깨 관절의 움직임 중 하나로, 전완 (아래팔) 이 뒤쪽 (외측) 으로 젖혀지는 것
> - 최대로 된 상태를 `Arm Cocking` 이라 부름
> - `+` 값이 증가할수록 전완이 많이 젖혀져 arm cocking 의 크기가 큰 상태
> - 값이 클수록 구속과 관련이 있지만, 과도한 각도는 부상 위험이 있음

- ___Shoulder Horizontal Abduction___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/SHA.png" width = 600>

> - 어깨 관절의 움직임 중 하나로, 위팔을 뒤쪽 (후면) 방향으로 움직이는 것
> - 공을 던지기 위하여 팔을 뒤로 보낼 때, 어깨가 열리는 동작
> - 견갑이 모아진 정도를 말하는 `견갑골 장전 (Scap Load)` 와 관련
> - `-` 값이 증가할수록 팔을 뒤쪽으로 많이 보내 견갑골 장전의 정도가 큰 것을 의미


### Arm Acceleration Phase
- ___Head - Hand Distance___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/HeadHandDist.png" width = 600>

> - `BR` 에서의 귀와 손 사이의 거리

- ___Shoulder Abduction___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/SHOAB.png" width = 600>

> - 어깨 관절의 움직임 중 하나로, 공을 던지기 위하여 몸의 옆쪽으로 팔을 들어 올린 정도
> - 앞에서 보았을 때, 몸의 중심축에서 팔이 옆으로 벌어진 각도
> - `+` 값으로 증가할수록 팔이 옆으로 많이 벌어짐 (들어 올림)
> - `BR`에서 어떤 수치인지가 중요하며 80 ~ 110° 사이가 권장되며, 그 이상이 될 경우 어깨 관절 부상을 조심해야할 수 있음

- ___Trunk Forward Tilt___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/TFT.png" width = 600>

> - 몸통이 앞쪽으로 숙여진 각도
> - 곧게 서있는 몸통 각도를 0° 라고 했을 때, 앞쪽으로 숙여질수록 `+` 값이 증가


- ___Trunk Lateral Tilt___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/TLT.png" width = 600>

> - 몸통이 옆으로 기울어진 각도
> - 곧게 서있는 몸통 각도를 0° 라고 했을 때, 던지는 팔 반대 방향으로 기울어질수록 `+` 값으로, 던지는 팔 방향으로 기울어질수록 `-` 값으로 증가
> - 과도한 각도는 제구력의 문제 또는 어깨 부상에 취약한 문제가 있을 수 있음


- ___Lead Leg Knee Flexion___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/LeadKneeFlex.png" width = 600>

> - `Arm Acceleration Phase`에서 앞 다리 (디딤 발) 의 무릎이 굽혀진 정도
> - `+` 값으로 증가할수록 앞 다리 (디딤 발) 의 무릎이 많이 굽혀짐
> - `FC`에서 `MER`로 진행될 때 살짝 굽혀지며, `MER`에서 `BR`로 진행될 때 무릎이 펴짐
> - `FC`에서 `MER`로 진행될 때 과도하게 굽혀지면 Stretch - Shortening Cycle `SSC` 를 잘 활용하지 못해 하체에서 폭발적임 힘을 사용하지 못하게 될 수 있음

- ___Lead Leg Knee Extention Angular Velocity___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/LeadKneeFlexVel.png" width = 600>

> - 앞 다리 (디딤 발) 의 무릎이 펴지는 각속도
> - 값이 클수록 앞 다리 (디딤 발) 의 무릎이 펴지는 각속도가 빠르다는 의미
> - 구속과 관련있는 변인 중 하나

- ___Lead Leg GRF (AP axis)___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/leadgrfAP.png" width = 600>

> - 흔히 제동력 (Braking Force) 라고 함
> - 앞 다리 (디딤 발) 가 발의 앞 - 뒤 (타자 - 2루) 방향으로 지면을 밀어내는 힘의 크기
> - `+` 값으로 증가할수록 앞쪽 (타자), `-` 값으로 증가할수록 뒤쪽 (2루) 으로 지면을 밀어냄
> - 즉, `-` 값으로 클수록 제동력이 좋은 투수라고 할 수 있음
> - 구속과 정적 상관관계가 있는 변인 중 하나

- ___Lead Leg GRF (Vertical)___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/pitching/leadgrfV.png" width = 600>

> - 앞 다리 (디딤 발) 가 지면의 수직 방향으로 지면을 밀어내는 힘의 크기
> - `+` 값으로 증가할수록 더 큰 힘으로 지면을 밀어냄
> - 자신 체중의 2배 이상은 좋은 수치라 할수 있음
> - 구속과 정적 상관관계가 있는 변인 중 하나
---


## 타자 리포트 (Hitting Report)

### 분석 구간

<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/hitting_analysis.png" width = 600>

- 시점
    1. Toe Off `TO` : 앞 발을 지면에서 떨어졌을 때
    2. Knee High `KH` : 앞 다리의 무릎을 최대로 들어올렸을 때
    3. Foot Contact `FC` : 앞 발이 지면과 접촉하였을 때
    4. Ball Impact `BI` : 공을 임팩트 했을 때

- 구간
    1. Loading Phase : `TO`와 `KH` 사이의 시간으로 뒷 발에 체중을 싣는 구간.
    2. Stride Phase : `KH`와 `FC` 사이의 시간으로 투수 방향으로 추진하는 구간
    3. Swing Phase : `FC`와 `BC` 사이의 시간으로 타자가 스윙하는 구간
---

### Swing Efficiency

- ___Kinematic Sequence___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/kinematic.png" width = 600>

> - 분절 (`골반, 몸통, 팔`) 회전 순서와 속도
> - 몸 전체 속도를 생성하고 전달할 때 ___효율적인 순서___ : `골반 -> 몸통 -> 팔`
> - 몸통은 골반을 기반으로 가속하고 골반은 감속, 팔은 몸통을 기반으로 가속하고 몸통은 감속하여 회전력을 전달하는 것이 효율적 : 빨간색 (골반) 그래프의 피크점을 타고 올라가 초록색 (몸통) 그래프가 올라가고, 초록색 (몸통) 그래프의 피크점을 타고 올라가 파란색 (팔) 그래프가 올라가는 것이 이상적
>- `Speed Gain` : `다음 분절 최대 각속도 / 이전 분절 최대 각속도`로 얻을 수 있는 수치며, 1.4 이상이 이전 분절이 다음 분절로 회전 전달이 좋은 수치로 이루어졌다는 것을 의미함

- ___X-Factor___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/xfactor.png width = 600>
  
> - 회전을 통하여 골반 (Hip) 과 어깨 (Shoulder) 사이의 분리된 각도 차이
> - 하체 (엉덩이) 와 상체 (어깨) 가 꼬인 정도
> - `-` 값으로 증가할수록 꼬임 정도가 큰 것을 의미
> - 과도한 꼬임 각도는 회전 능력이 없으면 타격 타이밍에 영향을 줄수 있음
> - `FC` 이후에 최대 꼬임이 나타나는 것이 좋은 타이밍이라 할수 있음

- ___Stride Length___
<img src="https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/stride.png" width = 200>

> - 공을 타격할 때 발을 내딛는 거리로 `FC`에서 뒷 발과 앞 발의 거리
> - 타자의 키에 대한 `%` 로 표현
---

### Loading Phase

- ___Sway [Shank Angle]___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/sway.png width = 600>

> - `Sway (스웨이)`는 `Loading Phase` 중에 체중이 투수 반대 방향으로 움직이는 것을 의미
> - 정강이 각도가 투수 반대 방향으로 얼마나 기울어졌는지를 관찰
> - `Loading Phase`에서 `-` 값이 있으면 `Sway` 로 판단

- ___Rear Leg Torque___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/rearlegtorq.png width = 600>

> - 뒷 다리 (축 다리) 가 스윙 동작 중에 발생하는 회전력으로 스윙의 힘과 안정성을 증가하는데 중요한 역할을 함
> - `Loading Phase`에서 `45Nm 이상`이면 좋은 수치라고 할 수 있음

---

### Stride Phase

- ___Loss Of Posture [Trunk Lateral Tilt]___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/lossofposture_tlt.png width = 600>

> - 스윙 중 올바른 자세를 만들고 유지하지 못함을 의미
> - `Loss of Posture`가 얼마나 나타났는지 알기 위해 몸통이 옆쪽으로 얼마나 기울어졌는지를 관찰
> - `+` 값이 증가할수록 타격하는 타격하는 홈플레이트 방향으로 기울어짐

- ___Rear Leg AP GRF___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/rearlegapgrf.png width = 600>

> - 뒷 다리 (축 다리) 가 지면과 수직인 방향으로 밀어내는 힘의 크기를 의미
> - `Loading Phase`에서 자신의 체중의 98% 이상이 좋은 수치라고 할 수 있음

---

### Swing Phase

- ___Dead Hands [Lead Shoulder - Hand Distance]___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/deadhands.png width = 600>

> - `Dead Hands`는 `FC`에서 두 손의 위치 변화가 없거나 감소하는 것
> - 어깨 라인과 손의 거리가 충분히 멀어지는지 관찰
> - 어깨와 손이 같은 라인에 있을 때 '0'
> - `-` 값으로 증가할수록 손이 어깨 뒤쪽으로 멀어지고, `+` 값으로 증가할수록 손이 어깨 앞쪽으로 멀어지는 것을 의미

- ___Casting The Hands [Elbow Flexion]___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/castinghand.png width = 600>

> - `Casting The Hands`는 스윙 시작 시 손과 팔꿈치 사이의 관계
> - 스윙의 약 1/3 동안 손이 팔꿈치보다 몸에 더 가깝게 유지되어야 함
> - 일찍 팔꿈치를 펴게 되면 공을 임팩트 할 때, 배트 속도를 감소시킴


- ___Loss Of Space___
    - 타자가 투구 라인을 따라 스윙을 할 수 있는 공간을 만들고 유지하지 유지하지 못하는 것
    <br/><br/>

    1. ___Pelvis Open Timing___
    <img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/lossofspace1.png width = 600>

    > - `Loss of Space`를 확인하기 위해 골반이 언제 열리는지를 관찰
    > - `+` 값으로 급격하게 증가하는 시점이 골반이 열리는 시점

    2. ___Lead Shoulder - Hand  Distance___
    <img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/lossofspace2.png width = 600>

    > - `Loss of Space`를 확인하기 위해 어깨와 손 사이의 거리를 관찰하여 공간이 얼마나 있는지 관찰
    > - `+` 값으로 증가할수록 스윙 공간이 넓다는 것을 의미

    3. ___Elbow Height___
    <img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/lossofspace3.png width = 600>

    > - `Loss of Space`를 확인하기 위해 스윙 중 팔꿈치의 높이를 관찰
    > - `+`값으로 증가할수록 팔꿈치가 높게 들려 있는 것을 의미


- ___Lead Leg Ground Reaction Force (Vertical)___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/leadleggrfvertical.png width = 600>

> - 앞 다리 (디딤 발)가 지면과 수직인 방향으로 밀어내는 힘의 크기
> - `체중의 180%` 이상이면 좋은 수치라 할 수 있음

- ___Lead Leg Torque___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/leadlegtq.png width = 600>

> - 앞 다리 (디딤 발)가 스윙 동작 중 발생시키는 회전력으로 스윙의 안정성과 힘과 관련됨
> - `Swing Phase`에서 `100 Nm 이상`이면 좋은 수치라 할 수 있음

- ___Rear & Lead Leg Ground Reaction Force (AP axis)___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/grf_ap.png width = 600>

> - 타자의 앞 - 뒤 방향 (투수 - 포수 방향)으로 지면을 밀어내는 힘의 크기
> - `Rear` : `+`는 뒷 다리가 앞으로 추진하는 힘
> - `Lead` : `+`는 앞 다리가 추진하는 신체를 제동 (braking) 하는 힘 (포수 방향) [체중의 70% 이상이 좋은 수치]
> - `X-Axis Timing` : `100 * Rear의 최대 값 / Lead의 최대 값 시점의 Rear 값`으로 구할 수 있고 뒷 다리와 앞 다리의 적절한 체중이동을 확인하려고 하는 변인 [`80% 이상`이 효율적인 체중 이동]

- ___Rear Shoulder Ad/Abduction Angular Velocity___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/rearshoadvel.png width = 600>

> - 뒷 팔이 몸의 옆쪽으로 모으거나 벌릴 때의 각속도
> - `+` 값이 클수록 팔이 몸 쪽으로 빠르게 모아졌다는 것을 의미하고, `-` 값이 클수록 팔이 몸 바깥쪽으로 빠르게 벌려졌다는 것을 의미

- ___Lead Leg Knee Extension Angular Velocity___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/leadlegkneeextvel.png width = 600>

> - 앞 다리 (디딤 발)의 무릎이 펴지는 각속도
> - `+` 값이 클수록 무릎의 펴는 속도가 크다는 것을 의미

- ___Lead Elbow Extension Angular Velocity___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/leadelbowextvel.png width = 600>

> - 앞 팔의 팔꿈치가 펴지는 각속도
> - `+` 값이 클수록 앞 팔의 팔꿈치의 펴지는 각속도가 빠르다는 것을 의미

- ___Trunk Lateral Tilt___
<img src=https://github.com/parkdragonstone/kookmin-report-explain/blob/master/img/hitting/trunklateraltilt.png width = 600>

> - 몸통이 곧게 서있을 때가 0° 이며, 우타자의 경우 오른쪽 방향으로 기울어지면 `+`, 좌타자의 경우 왼쪽 방향으로 기울어지면 `+`