"""
India Constituency Data (Lok Sabha)

Provides real names and states for all 543 PCs.
"""

from electoral_sim.core.constituency import ConstituencyManager, ConstituencyMetadata

# Sample of major constituencies across states for the 543 seats
# Format: (State, [Const Names])
INDIA_PC_NAMES = {
    "Uttar Pradesh": [
        "Varanasi",
        "Lucknow",
        "Amethi",
        "Rae Bareli",
        "Gorakhpur",
        "Prayagraj",
        "Agra",
        "Kanpur",
        "Meerut",
        "Ghaziabad",
        "Noida",
        "Aligarh",
        "Mathura",
        "Ayodhya",
        "Jhansi",
        "Bareilly",
    ],
    "Maharashtra": [
        "Mumbai South",
        "Mumbai North",
        "Pune",
        "Nagpur",
        "Nashik",
        "Thane",
        "Baramati",
        "Aurangabad",
    ],
    "West Bengal": [
        "Kolkata South",
        "Kolkata North",
        "Diamond Harbour",
        "Jadavpur",
        "Asansol",
        "Darjeeling",
        "Howrah",
    ],
    "Tamil Nadu": [
        "Chennai South",
        "Chennai North",
        "Madurai",
        "Coimbatore",
        "Thoothukudi",
        "Kanyakumari",
    ],
    "Karnataka": [
        "Bangalore South",
        "Bangalore North",
        "Bangalore Central",
        "Mysore",
        "Hubli-Dharwad",
    ],
    "Gujarat": ["Gandhinagar", "Ahmedabad West", "Ahmedabad East", "Surat", "Rajkot", "Vadodara"],
    "Kerala": ["Wayanad", "Thiruvananthapuram", "Ernakulam", "Kozhikode", "Thrissur"],
    "Delhi": [
        "New Delhi",
        "South Delhi",
        "North East Delhi",
        "East Delhi",
        "West Delhi",
        "North West Delhi",
        "Chandni Chowk",
    ],
}


def get_india_constituencies() -> ConstituencyManager:
    """
    Returns Manager initialized with all 543 India Parliamentary Constituencies.
    Fillers are used for less prominent names to reach exact 543 count.
    """
    from electoral_sim.presets.india.election import INDIA_STATES

    ls_seats = []
    const_id = 0

    for state, total_seats in INDIA_STATES.items():
        known_names = INDIA_PC_NAMES.get(state, [])
        for i in range(total_seats):
            if i < len(known_names):
                name = known_names[i]
            else:
                name = f"{state} PC {i+1}"

            ls_seats.append(
                ConstituencyMetadata(
                    id=const_id, name=name, state=state, type="General"  # Simplified
                )
            )
            const_id += 1

    return ConstituencyManager(ls_seats)
